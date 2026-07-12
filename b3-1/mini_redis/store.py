"""Mini Redis 핵심 저장소 엔진.

hashmap.py(HashMap) + linked_list.py(DoublyLinkedList) + heap.py(MinHeap)
세 자료구조를 조합해 다음을 제공한다.

  - String Key-Value 저장/조회/삭제
  - O(1) LRU(Least Recently Used) 추적과, 메모리 초과 시 자동 제거
  - 힙 기반 TTL(만료 시간) 관리

이 클래스는 "무엇을 저장하고 어떻게 지울지"라는 규칙만 담당하고,
사용자 입력을 어떻게 읽을지·화면에 어떻게 보여줄지는 cli.py가
담당한다(관심사 분리).

dict/set/collections는 사용하지 않는다. 모든 매핑은 HashMap,
모든 정렬된 접근은 MinHeap, 모든 순서 추적은 DoublyLinkedList로 구현한다.
"""

import time

from mini_redis.hashmap import HashMap
from mini_redis.linked_list import DoublyLinkedList
from mini_redis.heap import MinHeap


class OOMError(Exception):
    """단일 키+값 크기가 maxmemory를 초과해 저장할 수 없을 때 발생시키는 예외."""


class MemoryInfo:
    """INFO memory 출력을 위한 값 객체 (dict 대신 사용하는 작은 클래스)."""

    __slots__ = ("used_memory", "maxmemory", "evicted_keys")

    def __init__(self, used_memory: int, maxmemory: int, evicted_keys: int):
        self.used_memory = used_memory
        self.maxmemory = maxmemory
        self.evicted_keys = evicted_keys


class _ValueEntry:
    """저장소에 실제로 들어가는 한 칸: 값 + 만료 시각(없으면 None)."""

    __slots__ = ("value", "expire_at")

    def __init__(self, value: str, expire_at=None):
        self.value = value
        self.expire_at = expire_at  # None이면 만료 시간 없음, 아니면 UNIX epoch(float)


def _byte_len(s: str) -> int:
    """UTF-8 인코딩 기준 바이트 길이. used_memory = Σ(len(utf8(key))+len(utf8(value)))."""
    return len(s.encode("utf-8"))


class MiniRedisStore:
    """Mini Redis의 핵심 엔진.

    내부에 총 4개의 자료구조를 들고 있다.

    self._map        : key -> _ValueEntry            (실제 데이터, HashMap)
    self._lru_list    : key들의 사용 순서               (DoublyLinkedList)
                        head = 가장 최근 사용, tail = 가장 오래 사용 안 함
    self._lru_nodes   : key -> self._lru_list의 Node   (HashMap)
                        "이 key가 LRU 리스트의 어느 노드인지"를 O(1)에 찾기
                        위한 보조 매핑. 이게 있어야 move_to_front/remove_node를
                        리스트 순회 없이 바로 호출할 수 있다 -> O(1) LRU.
    self._ttl_heap    : (expire_at, key) 최소 힙        (MinHeap)
                        "다음에 가장 먼저 만료될 키"를 O(log n)에 찾기 위함.
    """

    def __init__(self):
        self._map = HashMap()
        self._lru_list = DoublyLinkedList()
        self._lru_nodes = HashMap()
        self._ttl_heap = MinHeap()

        self._used_memory = 0
        self._maxmemory = 0  # 0 = 무제한
        self._evicted_keys = 0

    # ------------------------------------------------------------------
    # 내부 헬퍼: LRU
    # ------------------------------------------------------------------

    def _touch_lru(self, key: str) -> None:
        """key를 '방금 사용함'으로 기록한다. SET/GET '성공' 시에만 호출한다. O(1).

        이미 LRU 리스트에 있으면(=해시맵에서 O(1)로 노드를 바로 찾아)
        맨 앞으로 옮기고, 처음 보는 key면 맨 앞에 새로 삽입한다.
        """
        if self._lru_nodes.contains(key):
            node = self._lru_nodes.get(key)
            self._lru_list.move_to_front(node)
        else:
            node = self._lru_list.insert_front(key)
            self._lru_nodes.put(key, node)

    def _forget_lru(self, key: str) -> None:
        """key의 LRU 추적 정보를 제거한다 (DEL/만료/eviction 시 호출). O(1)."""
        if self._lru_nodes.contains(key):
            node = self._lru_nodes.get(key)
            self._lru_list.remove_node(node)
            self._lru_nodes.remove(key)

    # ------------------------------------------------------------------
    # 내부 헬퍼: 삭제(데이터+LRU+메모리 계정을 한 번에 정리)
    # ------------------------------------------------------------------

    def _remove_key(self, key: str) -> None:
        """데이터/LRU/메모리 계정에서 key를 완전히 제거한다.

        TTL 힙(self._ttl_heap)은 여기서 직접 건드리지 않는다. 힙 중간의
        특정 원소를 O(log n)에 지우는 것은 배열 기반 힙 구조상 번거롭기
        때문에(위치 추적이 추가로 필요), 대신 "lazy deletion" 전략을 쓴다:
        힙에는 이 key를 가리키는 '유령' 항목이 남아있을 수 있지만,
        나중에 힙에서 꺼낼 때(_purge_expired_from_heap) 현재 데이터와
        비교해서 더 이상 유효하지 않으면 그냥 버린다. 과제 명세에서도
        "lazy deletion 전략 등은 구현 선택"이라고 명시적으로 허용한다.
        """
        entry = self._map.get(key, None)
        if entry is None:
            return
        self._used_memory -= _byte_len(key) + _byte_len(entry.value)
        self._map.remove(key)
        self._forget_lru(key)

    # ------------------------------------------------------------------
    # 내부 헬퍼: TTL 만료 확인 (지연 삭제, lazy expiration)
    # ------------------------------------------------------------------

    def _is_expired(self, entry: _ValueEntry) -> bool:
        return entry.expire_at is not None and entry.expire_at <= time.time()

    def _expire_if_needed(self, key: str) -> bool:
        """key가 존재하지만 이미 만료되었다면 지금 삭제하고 True를 반환한다.

        모든 키 기반 명령어(GET/DEL/EXISTS/TTL/EXPIRE/SET의 덮어쓰기 확인)는
        실행 전에 이 메서드를 먼저 호출해, 만료된 키를 '없는 키'처럼
        취급해야 한다는 과제 규칙을 만족시킨다.
        """
        entry = self._map.get(key, None)
        if entry is None:
            return False
        if self._is_expired(entry):
            self._remove_key(key)
            return True
        return False

    def _purge_expired_from_heap(self) -> None:
        """힙의 꼭대기(가장 빨리 만료되는 항목)부터 확인하며 만료분을 정리한다.

        힙은 "지금 시각보다 expire_at이 작은 항목이 더 있는가?"를
        peek() 한 번(O(1))으로 확인할 수 있어서, 매 명령마다 전체 키를
        스캔(O(n))하지 않고도 실제로 만료된 것들만 골라 O(log n)씩
        정리할 수 있다. 이것이 "힙이 TTL 관리에 적합한 이유"의 핵심이다.

        lazy deletion: 힙에서 꺼낸 (expire_at, key)가 현재 데이터의
        expire_at과 정확히 일치할 때만 실제로 삭제한다. SET으로 TTL이
        초기화되었거나, EXPIRE로 새 만료 시각이 다시 설정된 경우
        힙에는 예전 '유령' 항목이 남아있을 수 있는데, 이런 항목은
        더 이상 유효하지 않으므로 조용히 버린다.
        """
        now = time.time()
        while self._ttl_heap.size() > 0:
            expire_at, key = self._ttl_heap.peek()
            if expire_at > now:
                break  # 가장 빠른 것도 아직 안 지났으면 나머지도 볼 필요 없음
            self._ttl_heap.pop()
            entry = self._map.get(key, None)
            if entry is not None and entry.expire_at == expire_at:
                self._remove_key(key)
            # else: 유령 항목(이미 삭제되었거나 TTL이 갱신됨) -> 그냥 버림

    # ------------------------------------------------------------------
    # String 명령어
    # ------------------------------------------------------------------

    def set(self, key: str, value: str) -> None:
        """SET key value.

        - 성공하면 정상적으로 저장하고 LRU를 갱신한다.
        - 기존 키를 덮어쓰는 경우 기존 TTL은 초기화(삭제)한다.
        - maxmemory > 0이고 이 (key, value) 하나만으로도 maxmemory를
          넘는다면, 아무것도 바꾸지 않고 OOMError를 던진다.
        - 그 외의 경우, 저장 후 used_memory가 maxmemory를 넘으면
          used_memory가 다시 maxmemory 이하가 될 때까지 LRU(가장 오래
          사용 안 한 키)부터 제거한다.
        """
        self._purge_expired_from_heap()
        self._expire_if_needed(key)

        new_entry_size = _byte_len(key) + _byte_len(value)
        if self._maxmemory > 0 and new_entry_size > self._maxmemory:
            raise OOMError()  # 이 시점까지는 아무 것도 변경하지 않았다

        existing = self._map.get(key, None)
        if existing is not None:
            self._used_memory -= _byte_len(key) + _byte_len(existing.value)

        self._map.put(key, _ValueEntry(value=value, expire_at=None))
        self._used_memory += new_entry_size
        self._touch_lru(key)

        self._evict_lru_until_under_limit(just_set_key=key)

    def _evict_lru_until_under_limit(self, just_set_key: str) -> None:
        """used_memory가 maxmemory 이하가 될 때까지 LRU 꼬리부터 제거한다.

        LRU 리스트의 tail = 가장 오래 사용되지 않은 키. 방금 SET/GET한
        키는 _touch_lru에 의해 이미 head로 옮겨졌으므로, 자기 자신이
        아직 다른 키가 남아있는 한 스스로를 지우는 일은 없다.
        """
        while self._maxmemory > 0 and self._used_memory > self._maxmemory:
            tail_node = self._lru_list.tail
            if tail_node is None:
                break
            victim_key = tail_node.data
            if victim_key == just_set_key and self._lru_list.size() == 1:
                # 방금 넣은 키 하나만 남았는데도 초과라면(이론상 set()의
                # 사전 검사 덕분에 발생하지 않는다) 무한 루프 방지용 안전장치.
                break
            self._remove_key(victim_key)
            self._evicted_keys += 1

    def get(self, key: str):
        """GET key. 없거나 만료됐으면 None, 있으면 value(str)를 반환한다.

        반환에 성공한 경우에만 LRU를 갱신한다(만료로 삭제된 경우는 갱신 안 함).
        """
        self._purge_expired_from_heap()
        if self._expire_if_needed(key):
            return None
        entry = self._map.get(key, None)
        if entry is None:
            return None
        self._touch_lru(key)
        return entry.value

    def delete(self, key: str) -> bool:
        """DEL key. 삭제했으면 True, 원래 없었으면(만료 포함) False."""
        self._purge_expired_from_heap()
        if self._expire_if_needed(key):
            return False  # 이미 만료되어 '없는 키'로 취급 -> 지울 대상 없음
        existed = self._map.contains(key)
        if existed:
            self._remove_key(key)
        return existed

    def exists(self, key: str) -> bool:
        """EXISTS key."""
        self._purge_expired_from_heap()
        if self._expire_if_needed(key):
            return False
        return self._map.contains(key)

    def dbsize(self) -> int:
        """DBSIZE. 현재 저장된(만료되지 않은) 키 개수."""
        self._purge_expired_from_heap()
        return self._map.size()

    def keys(self):
        """KEYS. 저장된 모든 키를 리스트로 반환한다. 순서는 보장하지 않는다."""
        self._purge_expired_from_heap()
        return self._map.keys()

    # ------------------------------------------------------------------
    # 메모리 관리
    # ------------------------------------------------------------------

    def config_set_maxmemory(self, bytes_limit: int) -> None:
        """CONFIG SET maxmemory bytes. 0이면 무제한."""
        self._maxmemory = bytes_limit

    def info_memory(self) -> MemoryInfo:
        """INFO memory. used_memory/maxmemory/evicted_keys를 담은 값 객체 반환."""
        self._purge_expired_from_heap()
        return MemoryInfo(
            used_memory=self._used_memory,
            maxmemory=self._maxmemory,
            evicted_keys=self._evicted_keys,
        )

    # ------------------------------------------------------------------
    # TTL 관리
    # ------------------------------------------------------------------

    def expire(self, key: str, seconds: int) -> bool:
        """EXPIRE key seconds. key가 없으면 False, 설정했으면 True.

        seconds <= 0이면 '즉시 만료'로 간주해 키를 바로 삭제한다
        (존재했다면 True를 반환한다).
        """
        self._purge_expired_from_heap()
        if self._expire_if_needed(key):
            return False
        entry = self._map.get(key, None)
        if entry is None:
            return False
        if seconds <= 0:
            self._remove_key(key)
            return True
        entry.expire_at = time.time() + seconds
        self._ttl_heap.push((entry.expire_at, key))
        return True

    def ttl(self, key: str) -> int:
        """TTL key. 없으면 -2, TTL 미설정이면 -1, 있으면 남은 초(정수)."""
        self._purge_expired_from_heap()
        if self._expire_if_needed(key):
            return -2
        entry = self._map.get(key, None)
        if entry is None:
            return -2
        if entry.expire_at is None:
            return -1
        remaining = int(entry.expire_at - time.time())
        return remaining if remaining > 0 else 0
