"""Mini Git 저장소 상태 관리: INIT / BRANCH / SWITCH / COMMIT + 조회 명령 위임.

이 클래스는 "지금 어떤 브랜치에 있는지, 각 브랜치의 HEAD가 어디를 가리키는지,
누가 커밋 중인지" 같은 저장소 상태만 관리한다. 그래프 탐색(위상 정렬/최단
경로/조상)은 traversal.py, 정렬은 sorting.py, 검색은 index.py에 위임한다 —
"알고리즘 로직은 독립된 함수/클래스로 분리한다"는 과제 제약을 그대로 반영한
구조다.

커밋 저장소 자체는 파이썬 dict(hash -> Commit)를 사용한다. 과제 제약상
dict/list/set은 자유롭게 쓸 수 있고(그래프 전용 라이브러리와 정렬 표준
API만 금지), dict는 정확히 "hash로 즉시 찾기(해시맵 기반 조회)"라는
명세를 그대로 만족한다.
"""

from datetime import datetime

from mini_git.commit import Commit, generate_commit_hash
from mini_git.errors import (
    InvalidArgsError,
    NotInitializedError,
    UnknownBranchError,
    UnknownCommitError,
)
from mini_git.index import InvertedIndex
from mini_git import sorting
from mini_git import traversal


class Repository:
    """Mini Git 저장소 하나(=REPL 세션 하나)의 전체 상태."""

    def __init__(self):
        self.commits = {}          # hash -> Commit  (커밋 그래프의 노드 저장소)
        self.branches = {}         # branch_name -> head commit hash (없으면 None)
        self.current_branch = None
        self.current_user = None
        self.initialized = False
        self.index = InvertedIndex()

    # ------------------------------------------------------------------
    # 내부 헬퍼
    # ------------------------------------------------------------------

    def _require_initialized(self) -> None:
        if not self.initialized:
            raise NotInitializedError()

    # ------------------------------------------------------------------
    # 저장소 / 브랜치 관리
    # ------------------------------------------------------------------

    def init(self, user_name: str) -> None:
        """INIT <user_name>: 저장소 초기화, main 브랜치 생성, 사용자 설정."""
        if not user_name:
            raise InvalidArgsError()
        self.commits = {}
        self.branches = {"main": None}
        self.current_branch = "main"
        self.current_user = user_name
        self.index = InvertedIndex()
        self.initialized = True

    def branch(self, name: str) -> None:
        """BRANCH <branch_name>: 현재 HEAD를 가리키는 새 브랜치를 만든다."""
        self._require_initialized()
        if not name:
            raise InvalidArgsError()
        head = self.branches[self.current_branch]
        self.branches[name] = head  # 이미 있는 이름이면 HEAD 위치로 재설정(단순화된 정책)

    def switch(self, name: str) -> None:
        """SWITCH <branch_name>: HEAD(현재 브랜치)를 name으로 옮긴다."""
        self._require_initialized()
        if not name:
            raise InvalidArgsError()
        if name not in self.branches:
            raise UnknownBranchError(name)
        self.current_branch = name

    def commit(self, message: str) -> Commit:
        """COMMIT <message>: 현재 HEAD를 부모로 하는 새 커밋을 만든다."""
        self._require_initialized()
        if not message:
            raise InvalidArgsError()

        parent_hash = self.branches[self.current_branch]
        parents = [parent_hash] if parent_hash is not None else []
        timestamp = datetime.now()

        commit_hash = generate_commit_hash(
            self.commits, message, self.current_user, timestamp, parents
        )
        new_commit = Commit(
            commit_hash=commit_hash,
            message=message,
            author=self.current_user,
            timestamp=timestamp,
            parents=parents,
            branch=self.current_branch,
        )

        self.commits[commit_hash] = new_commit
        self.branches[self.current_branch] = commit_hash
        self.index.add_commit(new_commit)
        return new_commit

    # ------------------------------------------------------------------
    # 로그 / 조회
    # ------------------------------------------------------------------

    def log(self):
        """LOG: 부모가 항상 자식보다 먼저 오는 순서(위상 정렬)로 커밋 목록 반환."""
        self._require_initialized()
        order = traversal.topological_order(self.commits)
        return [self.commits[h] for h in order]

    def log_sorted(self, by: str):
        """LOG --sort-by=date|author: 직접 구현한 병합 정렬로 정렬된 커밋 목록 반환."""
        self._require_initialized()
        if by not in ("date", "author"):
            raise InvalidArgsError()

        # 정렬 전 기준 순서(동률일 때 유지될 순서)로 위상 정렬 결과를 사용한다.
        base_order = [self.commits[h] for h in traversal.topological_order(self.commits)]

        if by == "date":
            key = lambda c: c.timestamp
        else:  # by == "author"
            key = lambda c: c.author

        return sorting.merge_sort(base_order, key)

    def ancestors(self, commit_hash: str):
        """ANCESTORS <commit_hash>: 도달 가능한 모든 조상 커밋 hash 리스트."""
        self._require_initialized()
        if commit_hash not in self.commits:
            raise UnknownCommitError(commit_hash)
        return traversal.ancestors(self.commits, commit_hash)

    def shortest_path(self, start_hash: str, end_hash: str):
        """PATH <commit1> <commit2>: 무방향 최단 경로(사전순 최소). 없으면 None."""
        self._require_initialized()
        if start_hash not in self.commits:
            raise UnknownCommitError(start_hash)
        if end_hash not in self.commits:
            raise UnknownCommitError(end_hash)
        return traversal.shortest_path(self.commits, start_hash, end_hash)

    def search_keyword(self, keyword: str):
        """SEARCH <keyword>: 역색인 기반 메시지 키워드 검색 -> Commit 리스트."""
        self._require_initialized()
        if not keyword:
            raise InvalidArgsError()
        hashes = self.index.search_keyword(keyword)
        return [self.commits[h] for h in hashes]

    def search_author(self, author: str):
        """SEARCH --author=<name>: 역색인 기반 작성자 검색 -> Commit 리스트."""
        self._require_initialized()
        if not author:
            raise InvalidArgsError()
        hashes = self.index.search_author(author)
        return [self.commits[h] for h in hashes]
