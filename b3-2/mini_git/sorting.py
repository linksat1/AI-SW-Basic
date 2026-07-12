"""정렬 알고리즘 직접 구현 (병합 정렬 / Merge Sort).

과제 제약: `sorted()`, `list.sort()` 등 파이썬 표준 정렬 API를 쓰지 않고
직접 구현해야 한다. 이 모듈은 병합 정렬을 일반화된 형태로 구현해
`LOG --sort-by=date`와 `LOG --sort-by=author` 양쪽에서 재사용한다
(비교 기준을 `key` 함수로 넘겨받아 바꿀 수 있다).

왜 병합 정렬을 골랐는가
    - 시간복잡도: 분할이 항상 정확히 반씩 이루어지므로 입력 데이터의
      배치와 무관하게 평균/최악 모두 O(n log n)이다. (퀵 정렬은 평균은
      O(n log n)이지만 이미 정렬된 입력 등 특정 상황에서 O(n^2)로
      나빠질 수 있다.)
    - 안정 정렬(Stable Sort): 두 원소의 비교 키가 같을 때, 병합 단계에서
      "왼쪽(원래 앞에 있던) 원소를 같을 때도 먼저 채택"하므로 원래
      순서가 유지된다. LOG --sort-by=author처럼 같은 작성자가 여러
      커밋을 가진 경우, 정렬 후에도 원래(위상 정렬 순서에 따른)
      순서가 그대로 보존되어 "동률 처리 규칙"이 직관적이고 재현 가능하다.
"""


def merge_sort(items, key):
    """items를 key(item) 기준 오름차순으로 정렬한 "새 리스트"를 반환한다.

    원본 items는 변경하지 않는다(list.sort()처럼 제자리 정렬이 아니다).
    시간복잡도 O(n log n), 공간복잡도 O(n), 안정 정렬.
    """
    n = len(items)
    if n <= 1:
        return list(items)

    mid = n // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)
    return _merge(left, right, key)


def _merge(left, right, key):
    """이미 정렬된 두 리스트 left, right를 하나의 정렬된 리스트로 합친다.

    `<=`(작거나 같으면 왼쪽을 먼저)를 써서, 두 값이 같을 때 항상 왼쪽
    리스트의 원소를 먼저 채택한다. 이 규칙이 병합 정렬을 "안정 정렬"로
    만드는 핵심이다.
    """
    merged = []
    i = j = 0
    len_left, len_right = len(left), len(right)

    while i < len_left and j < len_right:
        if key(left[i]) <= key(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # 둘 중 하나가 먼저 바닥나면, 남은 리스트는 이미 정렬되어 있으므로
    # 그대로 뒤에 이어 붙이면 된다.
    while i < len_left:
        merged.append(left[i])
        i += 1
    while j < len_right:
        merged.append(right[j])
        j += 1

    return merged
