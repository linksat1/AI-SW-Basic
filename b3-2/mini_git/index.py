"""역색인(Inverted Index).

"커밋 메시지에 이 단어가 들어있는 커밋을 찾아라" 같은 질의를 처리할 때,
매번 전체 커밋을 순회하며 메시지를 검사하면 커밋이 N개일 때 O(N)이 걸린다.
대신 "단어 -> 그 단어를 포함한 커밋 hash 목록"을 미리 만들어두면(역색인),
조회는 그 단어를 키로 해시맵에서 바로 찾기만 하면 되므로 평균 O(1) +
결과 개수만큼(O(k))이 걸린다. author 검색도 같은 원리다.

과제 제약상 dict/list/set은 자유롭게 사용할 수 있다(금지 대상은 그래프
전용 라이브러리와 정렬 표준 API뿐이다).
"""


class InvertedIndex:
    """keyword -> commit_hash 목록, author -> commit_hash 목록 두 종류의 역색인."""

    def __init__(self):
        self._keyword_index = {}  # {정규화된 단어: [commit_hash, ...]}
        self._author_index = {}   # {author: [commit_hash, ...]}

    def add_commit(self, commit) -> None:
        """새 커밋 하나를 두 인덱스에 반영한다. COMMIT 실행 시마다 호출된다.

        키워드 추출 기준(과제 명세): 메시지를 공백 기준으로 split한 뒤
        각 토큰을 lower()로 정규화해 키워드로 사용한다.
        """
        for token in commit.message.split():
            keyword = token.lower()
            if keyword not in self._keyword_index:
                self._keyword_index[keyword] = []
            self._keyword_index[keyword].append(commit.hash)

        if commit.author not in self._author_index:
            self._author_index[commit.author] = []
        self._author_index[commit.author].append(commit.hash)

    def search_keyword(self, keyword: str):
        """keyword(소문자 정규화)를 메시지에 포함한 커밋 hash 목록. 없으면 빈 리스트.

        전체 커밋을 순회하지 않고, 미리 만들어둔 keyword_index에서
        바로 꺼내오기만 하므로 평균 O(1) (+ 결과 복사 O(k)).
        """
        return list(self._keyword_index.get(keyword.lower(), []))

    def search_author(self, author: str):
        """해당 author의 커밋 hash 목록. 없으면 빈 리스트. 평균 O(1) 조회."""
        return list(self._author_index.get(author, []))
