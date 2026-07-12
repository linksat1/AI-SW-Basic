"""커밋 그래프 탐색 알고리즘: 위상 정렬(LOG) / 최단 경로(PATH) / 조상(ANCESTORS).

세 함수 모두 "commits" 딕셔너리(hash -> Commit)만 입력으로 받는 순수 함수라서
Repository 클래스의 다른 상태(현재 브랜치, 사용자 등)와 완전히 분리되어 있고,
독립적으로 테스트할 수 있다. 그래프 전용 라이브러리(networkx 등)는 쓰지 않고
BFS/큐 기반 알고리즘을 직접 구현했다.
"""


def topological_order(commits):
    """부모 커밋이 항상 자식 커밋보다 먼저 오도록 정렬된 커밋 hash 리스트를 반환한다.

    Git의 커밋 그래프는 "커밋 -> 부모"를 가리키는 간선들로 이루어진 DAG
    (방향성 비순환 그래프)다. 사이클이 없기 때문에 "부모가 먼저"라는 순서가
    항상 존재하고, 그 순서를 찾는 표준적인 방법이 위상 정렬이다.

    여기서는 Kahn의 알고리즘(진입차수 기반 BFS)을 사용한다.
      1) 각 커밋의 "진입차수"를 그 커밋이 가진 parents 개수로 정의한다
         (= "이 커밋이 출력되려면 먼저 출력돼야 하는 다른 커밋 수").
      2) 진입차수가 0인 커밋(=최초 커밋들)부터 큐에 넣는다.
      3) 큐에서 하나를 꺼내 결과에 추가하고, 그 커밋을 부모로 둔 자식들의
         진입차수를 1씩 깎는다. 0이 되는 순간 큐에 추가한다.
      4) 큐가 빌 때까지 반복하면, 부모가 항상 자식보다 먼저 나온 순서가 완성된다.

    동률(동시에 진입차수 0이 되는 경우) 처리: 큐는 선입선출(FIFO)이므로
    "먼저 진입차수 0이 된 순서 == 대체로 먼저 생성된 순서"가 그대로
    유지된다(리스트를 큐로 사용, 인덱스 포인터 방식이라 pop(0) 반복에
    따른 O(n^2)를 피하고 O(n)으로 동작한다).
    """
    children = {h: [] for h in commits}
    in_degree = {h: len(c.parents) for h, c in commits.items()}

    for h, c in commits.items():
        for p in c.parents:
            children[p].append(h)

    queue = [h for h in commits if in_degree[h] == 0]
    head = 0
    result = []

    while head < len(queue):
        current = queue[head]
        head += 1
        result.append(current)
        for child in children[current]:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                queue.append(child)

    return result


def ancestors(commits, commit_hash):
    """commit_hash에서 부모 방향으로 도달 가능한 모든 조상 hash를 찾는다 (자기 자신 제외).

    부모의 부모의 부모... 를 계속 따라가는 BFS다. DAG이므로 순환이 없어
    무한 루프 걱정 없이 종료하지만, 병합 커밋처럼 여러 경로로 같은 조상에
    도달할 수 있으므로 visited(set)로 중복 방문을 막는다.
    시간복잡도 O(V+E) (V=조상 수, E=조상들 사이의 부모-자식 간선 수).
    """
    visited = set()
    queue = list(commits[commit_hash].parents)
    result = []

    while queue:
        h = queue.pop(0)
        if h in visited:
            continue
        visited.add(h)
        result.append(h)
        queue.extend(commits[h].parents)

    return result


def _undirected_adjacency(commits):
    """"커밋-부모 연결을 무방향 간선으로 간주"한 인접 리스트를 만든다.

    PATH 명령의 정의(과제 명세)에 따라, 부모->자식 방향만 따라가는 게
    아니라 양쪽으로 다 이동할 수 있는 그래프를 별도로 구성한다.
    """
    adjacency = {h: [] for h in commits}
    for h, c in commits.items():
        for p in c.parents:
            adjacency[h].append(p)
            adjacency[p].append(h)
    return adjacency


def _bfs_distances(adjacency, source):
    """무방향 그래프에서 source로부터 모든 도달 가능한 노드까지의 최단 거리(간선 수)."""
    distance = {source: 0}
    queue = [source]
    head = 0
    while head < len(queue):
        node = queue[head]
        head += 1
        for neighbor in adjacency[node]:
            if neighbor not in distance:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    return distance


def shortest_path(commits, start_hash, end_hash):
    """start_hash에서 end_hash까지 "무방향 간선 기준" 최단 경로를 찾는다.

    반환값: 경로를 이루는 커밋 hash 리스트(start부터 end까지), 경로가 없으면 None.

    최단 경로가 여러 개 존재할 수 있는데(같은 부모에서 갈라진 두 브랜치의
    끝 커밋끼리 등), 과제 명세는 "hash1->hash2->... 문자열로 만들었을 때
    사전순이 가장 작은 경로"를 요구한다. 이를 위해:
      1) start와 end 양쪽에서 각각 BFS로 모든 노드까지의 거리를 구한다.
      2) start에서 시작해, "이 지점까지의 최단 거리 + 남은 최단 거리 합이
         전체 최단 거리 L과 같은" 이웃들(=반드시 어떤 최단 경로 위에 있는
         이웃들) 중에서 hash 문자열이 사전순으로 가장 작은 것을 매 걸음
         탐욕적으로 선택한다.
    각 단계에서 "가능한 다음 걸음 중 최소"를 고르는 것을, 목적지에 도착할
    때까지 반복하면 전체적으로 사전순이 가장 작은 경로가 완성된다(경로
    문자열은 첫 글자가 다른 지점부터 비교되므로, 앞쪽 선택이 작을수록
    전체 문자열도 작아지기 때문).
    """
    if start_hash not in commits or end_hash not in commits:
        return None
    if start_hash == end_hash:
        return [start_hash]

    adjacency = _undirected_adjacency(commits)
    dist_from_start = _bfs_distances(adjacency, start_hash)
    if end_hash not in dist_from_start:
        return None  # 두 커밋이 서로 다른 연결 요소에 있어 경로 자체가 없음

    dist_from_end = _bfs_distances(adjacency, end_hash)

    path = [start_hash]
    current = start_hash
    while current != end_hash:
        best_next = None
        for neighbor in adjacency[current]:
            on_shortest_path = (
                dist_from_start.get(neighbor) == dist_from_start[current] + 1
                and dist_from_end.get(neighbor) == dist_from_end[current] - 1
            )
            if on_shortest_path:
                if best_next is None or neighbor < best_next:
                    best_next = neighbor
        current = best_next
        path.append(current)

    return path
