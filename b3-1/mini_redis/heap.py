"""최소 힙(Min-Heap) 직접 구현.

TTL(만료 시간) 관리를 위해 "다음으로 가장 빨리 만료될 키가 무엇인지"를
빠르게 알아내는 데 쓰인다.

왜 힙인가?
    만료 시각이 가장 빠른 키를 찾으려고 매번 모든 키를 훑으면 O(n)이다.
    정렬된 리스트를 유지하면 조회는 빠르지만 삽입이 O(n)이 된다.
    최소 힙은 "완전 이진 트리" 모양을 유지하면서 "부모가 항상 자식보다
    작다(또는 같다)"는 규칙만 지키므로, 최솟값 조회는 O(1)(peek),
    삽입/삭제는 트리의 높이(log n)만큼만 움직이면 되어 O(log n)이다.
    자주 삽입되고 자주 "가장 빠른 만료"를 확인해야 하는 TTL 관리에
    이 성질이 정확히 들어맞는다.

완전 이진 트리를 배열로 표현하기
    "완전 이진 트리"는 마지막 레벨을 제외하면 모든 레벨이 꽉 차 있고,
    마지막 레벨은 왼쪽부터 채워지는 트리다. 이런 모양은 굳이 노드와
    포인터로 만들 필요 없이, 배열 인덱스만으로 부모/자식 관계를 계산할
    수 있다 (인덱스 i의 부모는 (i-1)//2, 왼쪽 자식은 2i+1, 오른쪽
    자식은 2i+2). 그래서 이 구현은 파이썬 list를 "완전 이진 트리의
    배열 표현"으로 사용한다 (해시맵의 dict 대체 금지와는 무관하게,
    힙 자체가 원래 배열 기반 자료구조다).

TTL과의 연결
    이 힙에는 (expire_at, key) 튜플을 넣는다. 파이썬 튜플은 첫 번째
    원소부터 비교하므로, 별도의 비교자를 만들지 않아도 expire_at이
    가장 작은(=가장 먼저 만료되는) 항목이 항상 힙의 꼭대기(root)에
    온다.
"""


class MinHeap:
    """배열(list) 기반 이진 최소 힙."""

    def __init__(self):
        self._data = []  # 완전 이진 트리를 배열로 표현

    def __len__(self):
        return len(self._data)

    def size(self) -> int:
        """현재 담고 있는 원소 개수."""
        return len(self._data)

    def peek(self):
        """가장 작은 원소를 제거하지 않고 확인한다 (비어있으면 None). O(1)."""
        if not self._data:
            return None
        return self._data[0]

    def push(self, item) -> None:
        """새 원소를 삽입한다. O(log n).

        일단 배열 맨 끝에 붙인 뒤(완전 이진 트리 모양 유지),
        부모와 비교해가며 위로 올려보내 힙 속성을 복원한다.
        """
        self._data.append(item)
        self._heapify_up(len(self._data) - 1)

    def pop(self):
        """가장 작은 원소를 제거하고 반환한다 (비어있으면 None). O(log n).

        루트(가장 작은 값)를 빼낸 자리에 배열의 마지막 원소를 옮겨
        놓고(트리 모양 유지), 아래로 내려보내며 힙 속성을 복원한다.
        """
        if not self._data:
            return None
        smallest = self._data[0]
        last = self._data.pop()  # 배열 맨 끝 원소 제거
        if self._data:
            self._data[0] = last
            self._heapify_down(0)
        return smallest

    # ------------------------------------------------------------------
    # 배열 인덱스로 부모/자식 계산
    # ------------------------------------------------------------------

    @staticmethod
    def _parent(i: int) -> int:
        return (i - 1) // 2

    @staticmethod
    def _left(i: int) -> int:
        return 2 * i + 1

    @staticmethod
    def _right(i: int) -> int:
        return 2 * i + 2

    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]

    # ------------------------------------------------------------------
    # 힙 속성 복원
    # ------------------------------------------------------------------

    def _heapify_up(self, i: int) -> None:
        """i번 위치의 값이 부모보다 작으면 계속 위로 교환한다.

        트리의 높이(log n)만큼만 올라가면 되므로 O(log n).
        """
        while i > 0:
            parent = self._parent(i)
            if self._data[i] < self._data[parent]:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _heapify_down(self, i: int) -> None:
        """i번 위치의 값을 자식들과 비교해 더 작은 자식과 계속 교환한다.

        트리의 높이(log n)만큼만 내려가면 되므로 O(log n).
        """
        n = len(self._data)
        while True:
            left, right = self._left(i), self._right(i)
            smallest = i
            if left < n and self._data[left] < self._data[smallest]:
                smallest = left
            if right < n and self._data[right] < self._data[smallest]:
                smallest = right
            if smallest == i:
                break
            self._swap(i, smallest)
            i = smallest
