"""커밋 노드(Commit)와 커밋 hash 생성.

Git의 실제 커밋도 "부모 커밋(들)에 대한 참조"만 들고 있는 노드이고, 그 노드들이
모여 그래프를 이룬다. 이 모듈은 그 노드 하나를 표현하는 Commit 클래스와,
세션 내에서 절대 겹치지 않는 hash를 만들어주는 함수를 담는다.
"""

import hashlib
import itertools

# 프로그램이 실행되는 동안 계속 증가하기만 하는 카운터.
# 같은 메시지/작성자/시각으로 커밋을 두 번 만들더라도 카운터 값이 다르므로
# 해시 입력 문자열 자체가 절대 겹치지 않는다 -> 중복 hash가 원천적으로 불가능하다.
_sequence_counter = itertools.count()


class Commit:
    """커밋 그래프의 한 노드.

    hash      : 이 커밋을 유일하게 식별하는 짧은 16진수 문자열
    message   : 커밋 메시지
    author    : 작성자
    timestamp : 생성 시각 (datetime 객체)
    parents   : 부모 커밋 hash의 리스트 (0개=최초 커밋, 1개=일반 커밋,
                2개=병합 커밋). 이 parents 참조들이 곧 그래프의 간선이다.
    branch    : 이 커밋이 만들어질 당시의 브랜치 이름 (LOG 출력용 메타데이터)
    """

    def __init__(self, commit_hash, message, author, timestamp, parents, branch):
        self.hash = commit_hash
        self.message = message
        self.author = author
        self.timestamp = timestamp
        self.parents = list(parents)  # 항상 새 리스트로 복사해 외부 변형과 분리
        self.branch = branch

    def formatted_timestamp(self) -> str:
        """LOG 등에서 사람이 읽기 쉬운 "YYYY-MM-DD HH:MM:SS" 형태로 변환."""
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")


def generate_commit_hash(existing_hashes, message, author, timestamp, parents):
    """세션 내에서 유일한 짧은 커밋 hash를 만든다.

    커밋 내용(메시지/작성자/시각/부모 목록)과, 호출될 때마다 무조건 커지는
    시퀀스 번호를 합쳐 SHA-1으로 해싱한 뒤 앞 6자리만 사용한다. 시퀀스 번호가
    섞여 있어 완전히 동일한 커밋을 두 번 만들어도 해시 입력이 달라지므로
    이론적으로도 중복이 발생하지 않는다. 그럼에도 만에 하나(6자리 16진수=
    약 1,677만 가지) 충돌이 나면 시퀀스를 다시 뽑아 재시도한다(방어적 코드).
    """
    while True:
        seq = next(_sequence_counter)
        raw = "{}|{}|{}|{}|{}".format(
            message, author, timestamp.isoformat(), ",".join(parents), seq
        )
        digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:6]
        if digest not in existing_hashes:
            return digest
