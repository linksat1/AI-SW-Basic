"""역색인(Inverted Index).

"커밋 메시지에 이 단어가 들어있는 커밋을 찾아라" 같은 질의를 처리할 때,
매번 전체 커밋을 순회하며 메시지를 검사하면 커밋이 N개일 때 O(N)이 걸린다.
대신 "단어 -> 그 단어를 포함한 커밋 hash 목록"을 미리 만들어두면(역색인),
조회는 그 단어를 키로 해시맵에서 바로 찾기만 하면 되므로 평균 O(1) +
결과 개수만큼(O(k))이 걸린다. author 검색도 같은 원리다.
공백 포함 구문은 가장 드문 단어의 후보에서만 연속 토큰을 확인하며,
구문 길이 q와 후보 토큰 수 합 T에 대해 검사 비용은 최악 O(T*q)다.
검색어 정규화와 해싱 비용은 입력 길이에 따라 추가된다.

과제 제약상 dict/list/set은 자유롭게 사용할 수 있다(금지 대상은 그래프
전용 라이브러리와 정렬 표준 API뿐이다).
"""


class InvertedIndex:
    """keyword -> commit_hash 목록, author -> commit_hash 목록 두 종류의 역색인."""

    def __init__(self):
        self._keyword_index = {}  # {정규화된 단어: [commit_hash, ...]}
        self._author_index = {}   # {author: [commit_hash, ...]}
        self._message_tokens = {}  # {commit_hash: 정규화된 메시지 토큰 튜플}

    def add_commit(self, commit) -> None:
        """새 커밋 하나를 두 인덱스에 반영한다. COMMIT 실행 시마다 호출된다.

        키워드 추출 기준(과제 명세): 메시지를 공백 기준으로 split한 뒤
        각 토큰을 lower()로 정규화해 키워드로 사용한다.
        """
        tokens = tuple(token.lower() for token in commit.message.split())
        self._message_tokens[commit.hash] = tokens
        # 같은 단어가 반복되어도 한 커밋은 검색 결과에 한 번만 등장한다.
        for keyword in dict.fromkeys(tokens):
            if keyword not in self._keyword_index:
                self._keyword_index[keyword] = []
            self._keyword_index[keyword].append(commit.hash)

        if commit.author not in self._author_index:
            self._author_index[commit.author] = []
        self._author_index[commit.author].append(commit.hash)

    def search_keyword(self, keyword: str):
        """단어 또는 연속된 토큰 구문을 검색한다. 대소문자와 공백 수는 무시한다.

        한 단어는 역색인에서 바로 조회한다. 구문은 가장 드문 단어의
        후보 커밋만 검사하여 단어의 순서와 반복 횟수까지 확인한다.
        전체 커밋 순회는 하지 않으며 결과는 커밋 생성 순서를 유지한다.
        """
        query = tuple(token.lower() for token in keyword.split())
        if not query:
            return []
        if len(query) == 1:
            return list(self._keyword_index.get(query[0], []))

        candidates = None
        for token in query:
            posting = self._keyword_index.get(token, [])
            if not posting:
                return []
            if candidates is None or len(posting) < len(candidates):
                candidates = posting

        results = []
        width = len(query)
        for commit_hash in candidates:
            tokens = self._message_tokens[commit_hash]
            if any(tokens[i:i + width] == query
                   for i in range(len(tokens) - width + 1)):
                results.append(commit_hash)
        return results

    def search_author(self, author: str):
        """해당 author의 커밋 hash 목록. 평균 O(1) 조회 + O(k) 결과 복사."""
        return list(self._author_index.get(author, []))
