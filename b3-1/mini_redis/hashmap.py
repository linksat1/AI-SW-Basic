"""체이닝 방식 해시맵(HashMap) 직접 구현.

Mini Redis의 키-값 저장소, LRU 키→노드 매핑 등 여러 곳에서 재사용된다.

과제 제약에 따라 dict/set/collections를 전혀 쓰지 않는다. 대신
  - 버킷 테이블: 파이썬 list를 "고정 길이 배열(인덱스로만 접근)"처럼만 사용
  - 충돌 해결(체이닝): linked_list.py의 DoublyLinkedList를 재사용
로 직접 구현한다.
"""

from mini_redis.linked_list import DoublyLinkedList

_INITIAL_CAPACITY = 8
_LOAD_FACTOR = 0.75

# get()에서 "값이 원래 없었다"를 표현하기 위한 전용 표시자.
# None도 정상적인 저장 값일 수 있으므로 None과 구분하기 위해 별도 객체를 쓴다.
_MISSING = object()


class _Entry:
    """버킷 체인 안에 들어가는 키-값 한 쌍을 표현하는 내부 클래스."""

    __slots__ = ("key", "value")

    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashMap:
    """체이닝 방식 해시맵.

    해시 함수
        문자열 키를 대상으로 한 다항식 롤링 해시를 직접 설계했다.
        h = h * 31 + ord(문자) 를 각 글자마다 누적한 뒤 버킷 개수로
        나눈 나머지를 인덱스로 쓴다. 31을 곱하는 이유는 홀수(2의 배수가
        아님)이면서 시프트/뺄셈으로 최적화하기 좋은 소수라서 문자열
        해시에서 관례적으로 널리 쓰이기 때문이다(Java String.hashCode와
        동일한 방식). 곱셈이 누적되므로 문자 하나만 달라져도, 혹은 같은
        문자라도 위치가 다르면 해시값이 크게 달라져 충돌을 줄여준다.

    충돌 해결
        서로 다른 키가 같은 버킷 인덱스로 매핑되면(충돌), 그 버킷에
        이중 연결 리스트를 두고 (key, value) 쌍을 매달아 체이닝한다.

    확장
        저장된 개수 / 버킷 개수(로드 팩터)가 0.75를 넘으면 버킷 수를
        2배로 늘리고 모든 항목을 다시 해싱해 옮긴다. 버킷이 너무 적으면
        체인이 길어져 평균 O(1)이 O(n)에 가까워지므로, 로드 팩터를
        일정 수준 이하로 유지해야 성능이 보장된다.
    """

    def __init__(self, capacity: int = _INITIAL_CAPACITY):
        self._capacity = capacity
        self._buckets = [None] * capacity  # 각 칸은 None 또는 DoublyLinkedList
        self._size = 0

    def __len__(self):
        return self._size

    def size(self) -> int:
        """저장된 키의 개수."""
        return self._size

    # ------------------------------------------------------------------
    # 해시 함수 (직접 설계)
    # ------------------------------------------------------------------

    @staticmethod
    def _hash_string(key: str) -> int:
        """문자열 키에 대한 다항식 롤링 해시.

        h_0 = 0
        h_i = h_(i-1) * 31 + ord(key[i])

        32비트 범위로 마스킹해 파이썬의 임의 정밀도 정수가 계속
        커지는 것을 막는다(값 자체의 정확성과는 무관, 계산량만 절약).
        """
        h = 0
        for ch in key:
            h = (h * 31 + ord(ch)) & 0xFFFFFFFF
        return h

    def _bucket_index(self, key: str) -> int:
        return self._hash_string(key) % self._capacity

    def _find_node(self, key: str):
        """key가 들어있는 (버킷 인덱스, 노드)를 찾는다. 없으면 노드는 None.

        평균적으로는 버킷 하나에 항목이 거의 없어 O(1)이지만, 최악의
        경우(모든 키가 같은 버킷으로 몰림)에는 체인 길이만큼 순회하므로
        O(n)이 된다. 로드 팩터를 0.75 이하로 유지하는 이유가 바로
        이 최악의 경우를 확률적으로 방지하기 위함이다.
        """
        idx = self._bucket_index(key)
        chain = self._buckets[idx]
        if chain is None:
            return idx, None
        node = chain.head
        while node is not None:
            if node.data.key == key:
                return idx, node
            node = node.next
        return idx, None

    # ------------------------------------------------------------------
    # 공개 API: put / get / remove / contains / keys / size
    # ------------------------------------------------------------------

    def put(self, key: str, value) -> None:
        """key에 value를 저장한다. 이미 있는 key면 값만 갱신한다. 평균 O(1)."""
        idx, node = self._find_node(key)
        if node is not None:
            node.data.value = value  # 이미 있는 키 -> 갱신만
            return

        if self._buckets[idx] is None:
            self._buckets[idx] = DoublyLinkedList()
        self._buckets[idx].insert_back(_Entry(key, value))
        self._size += 1

        if self._size / self._capacity > _LOAD_FACTOR:
            self._resize(self._capacity * 2)

    def get(self, key: str, default=_MISSING):
        """key의 값을 반환한다.

        key가 없고 default를 넘기지 않았다면 KeyError를 던진다.
        default를 넘겼다면(예: get(key, None)) 그 값을 대신 반환한다.
        """
        _, node = self._find_node(key)
        if node is None:
            if default is _MISSING:
                raise KeyError(key)
            return default
        return node.data.value

    def contains(self, key: str) -> bool:
        """key가 존재하는지 여부. 평균 O(1)."""
        _, node = self._find_node(key)
        return node is not None

    def remove(self, key: str) -> bool:
        """key를 제거한다. 제거했으면 True, 원래 없었으면 False. 평균 O(1).

        체인 안에서 노드의 '위치'는 순회로 찾아야 하지만(그래서 평균
        O(1)), 일단 노드를 찾고 나면 DoublyLinkedList.remove_node가
        O(1)로 떼어낸다.
        """
        idx, node = self._find_node(key)
        if node is None:
            return False
        self._buckets[idx].remove_node(node)
        self._size -= 1
        return True

    def keys(self):
        """저장된 모든 key를 리스트로 반환한다. O(n). 순서는 보장하지 않는다."""
        result = []
        for chain in self._buckets:
            if chain is None:
                continue
            node = chain.head
            while node is not None:
                result.append(node.data.key)
                node = node.next
        return result

    # ------------------------------------------------------------------
    # 내부: 버킷 확장(리해싱)
    # ------------------------------------------------------------------

    def _resize(self, new_capacity: int) -> None:
        """버킷 배열을 new_capacity로 늘리고 기존 항목을 모두 재해싱한다.

        버킷 개수(capacity)가 바뀌면 '해시값 % capacity'로 계산하는
        인덱스도 전부 바뀌기 때문에, 단순히 배열만 늘리는 게 아니라
        모든 (key, value)를 다시 넣어야(rehash) 한다. O(n).
        """
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [None] * new_capacity
        self._size = 0
        for chain in old_buckets:
            if chain is None:
                continue
            node = chain.head
            while node is not None:
                self.put(node.data.key, node.data.value)
                node = node.next
