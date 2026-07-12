"""이중 연결 리스트(Doubly Linked List) 직접 구현.

Mini Redis에서 두 군데에 재사용된다.
  1. hashmap.py  : 같은 버킷에 몰린 키들을 체이닝(충돌 해결)하는 용도
  2. store.py    : LRU(Least Recently Used) 사용 순서를 추적하는 용도
                    (head = 가장 최근 사용, tail = 가장 오래 사용 안 함)

두 용도 모두 "노드를 이미 알고 있을 때 그 자리에서 바로 떼어내거나
맨 앞으로 옮길 수 있어야 O(1)"이라는 공통 요구가 있기 때문에,
연결 리스트 하나를 만들어 재사용하는 것이 자연스럽다.

dict/set 같은 내장 매핑 자료형은 전혀 사용하지 않는다.
"""


class Node:
    """이중 연결 리스트를 이루는 한 칸(노드).

    prev / next : 좌우로 이웃한 노드에 대한 참조 (없으면 None)
    data        : 이 노드가 들고 있는 실제 값 (임의의 파이썬 객체)
    """

    __slots__ = ("prev", "next", "data")

    def __init__(self, data):
        self.prev = None
        self.next = None
        self.data = data


class DoublyLinkedList:
    """head/tail 포인터를 유지하는 이중 연결 리스트.

    핵심 아이디어: 노드의 "위치"를 리스트를 처음부터 순회해서 찾는 게
    아니라, 이미 들고 있는 노드 참조(Node 객체)를 이용해 이웃 포인터만
    갈아 끼우면 되기 때문에 삽입/삭제/이동이 모두 O(1)이다.
    (반대로, "값으로 노드를 찾는" find 같은 연산은 이 클래스에 없다.
     그건 순회가 필요해 O(n)이므로, 값→노드 매핑은 해시맵이 담당하고
     이 클래스는 "노드를 손에 쥔 다음부터"의 O(1) 연산만 책임진다.)
    """

    def __init__(self):
        self.head = None  # 가장 앞 노드 (LRU에서는 "가장 최근 사용")
        self.tail = None  # 가장 뒤 노드 (LRU에서는 "가장 오래 사용 안 함")
        self._size = 0

    def __len__(self):
        return self._size

    def size(self) -> int:
        """현재 담고 있는 노드 개수."""
        return self._size

    def __iter__(self):
        """head -> tail 순서로 data를 순회한다 (디버깅/keys() 등에 사용)."""
        node = self.head
        while node is not None:
            yield node.data
            node = node.next

    # ------------------------------------------------------------------
    # 삽입
    # ------------------------------------------------------------------

    def insert_front(self, data) -> Node:
        """맨 앞에 새 노드를 삽입하고, 그 노드를 반환한다. O(1).

        호출한 쪽에서 반환된 Node를 들고 있으면, 나중에 remove_node나
        move_to_front를 O(1)에 호출할 수 있다.
        """
        node = Node(data)
        node.next = self.head
        if self.head is not None:
            self.head.prev = node
        self.head = node
        if self.tail is None:
            self.tail = node
        self._size += 1
        return node

    def insert_back(self, data) -> Node:
        """맨 뒤에 새 노드를 삽입하고, 그 노드를 반환한다. O(1)."""
        node = Node(data)
        node.prev = self.tail
        if self.tail is not None:
            self.tail.next = node
        self.tail = node
        if self.head is None:
            self.head = node
        self._size += 1
        return node

    # ------------------------------------------------------------------
    # 삭제
    # ------------------------------------------------------------------

    def remove_node(self, node: Node):
        """임의의 노드를 리스트에서 떼어낸다. O(1).

        node.prev / node.next를 이미 알고 있으므로, 리스트를 처음부터
        순회해서 위치를 찾을 필요가 전혀 없다. 이웃 두 노드의 포인터만
        서로를 가리키도록 갱신하면 끝난다. 이것이 배열이 아니라
        "연결 리스트"를 쓰는 이유이자, LRU 캐시가 O(1)로 동작하는 핵심이다.
        """
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next  # node가 head였던 경우

        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev  # node가 tail이었던 경우

        node.prev = None
        node.next = None
        self._size -= 1
        return node.data

    def remove_front(self):
        """맨 앞 노드를 제거하고 그 data를 반환한다 (비어있으면 None). O(1)."""
        if self.head is None:
            return None
        return self.remove_node(self.head)

    def remove_back(self):
        """맨 뒤 노드를 제거하고 그 data를 반환한다 (비어있으면 None). O(1)."""
        if self.tail is None:
            return None
        return self.remove_node(self.tail)

    # ------------------------------------------------------------------
    # 이동
    # ------------------------------------------------------------------

    def move_to_front(self, node: Node) -> Node:
        """이미 리스트 안에 있는 node를 맨 앞으로 옮긴다. O(1).

        LRU 캐시에서 "이 키를 방금 사용했다"는 사실을 기록할 때 사용한다.
        remove_node + insert_front를 각각 호출해도 되지만, 그러면 새
        Node 객체가 생겨서 해시맵이 들고 있던 Node 참조가 무효화된다.
        기존 Node 객체를 재사용해 포인터만 옮겨야 LRU 매핑이 계속 유효하다.
        """
        if self.head is node:
            return node  # 이미 맨 앞이면 할 일 없음

        # 1) 현재 위치에서 떼어낸다 (size는 그대로 유지)
        if node.prev is not None:
            node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev
        if self.tail is node:
            self.tail = node.prev

        # 2) 맨 앞에 다시 끼워 넣는다
        node.prev = None
        node.next = self.head
        if self.head is not None:
            self.head.prev = node
        self.head = node
        if self.tail is None:
            self.tail = node
        return node
