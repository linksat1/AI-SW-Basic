# Mini Git

커밋 그래프(DAG) / 위상 정렬 / 최단 경로(BFS) / 역색인 / 직접 구현한 병합
정렬로 만든 **CLI 기반 미니 버전 관리 시스템**입니다. 그래프 전용 라이브러리와
`sorted()`/`list.sort()` 같은 정렬 표준 API는 사용하지 않았습니다.

## 실행 방법

Python **3.10 이상**이 필요하며, 외부 패키지 설치는 필요 없습니다.
`b3-2` 폴더에서 실행하세요.

```bash
python main.py
```

`mini-git> ` 프롬프트가 뜨면 명령을 입력합니다. `exit` 또는 `quit`으로
종료합니다.

## 폴더 구조

```
b3-2/
├── main.py              ← 엔트리 포인트 (python main.py로 실행)
├── README.md             ← 이 문서
└── mini_git/
    ├── cli.py             REPL, 명령어 파싱, 출력 포맷팅
    ├── repository.py      저장소 상태(브랜치/HEAD/사용자) 관리 + 명령 위임
    ├── commit.py          Commit 노드 + 세션 내 유일한 hash 생성
    ├── traversal.py       위상 정렬(LOG) / 최단 경로(PATH) / 조상(ANCESTORS)
    ├── sorting.py          직접 구현한 병합 정렬 (LOG --sort-by)
    ├── index.py            역색인 (keyword/author -> commit hash 목록)
    └── errors.py           표준 오류 타입
```

## 지원 명령어

```
INIT <user_name>            BRANCH <branch_name>
SWITCH <branch_name>        COMMIT <message>

LOG                          LOG --sort-by=date
                              LOG --sort-by=author

PATH <commit1> <commit2>     ANCESTORS <commit_hash>

SEARCH <keyword>             SEARCH --author=<name>

exit / quit                  (REPL 종료)
```

- 명령어는 대소문자를 구분하지 않습니다 (`INIT`, `init` 모두 가능).
- 공백이 포함된 값은 큰따옴표로 감쌉니다: `COMMIT "Add login feature"`
- `SEARCH login`은 공백으로 분리된 단어 전체를 검색합니다. 부분 문자열 검색은 하지 않습니다.
- `SEARCH "login feature"`는 연속된 단어 구문을 검색합니다. 대소문자와 공백 수는 무시하지만 단어의 순서·반복 횟수는 구분합니다.
- 같은 단어가 메시지에 반복되어도 검색 결과에는 커밋이 한 번만 나옵니다.
- 작성자 검색은 이름 전체가 정확히 일치해야 합니다: `SEARCH --author="Alice Kim"`.
- 기존 브랜치 이름으로 `BRANCH`를 실행하면 `Invalid args`를 출력하며 HEAD를 보존합니다.
- `INIT`을 다시 실행하면 커밋·브랜치·역색인을 모두 초기화합니다.

## 검증 방법

```bash
python -B -m unittest discover -s tests -v
```

회귀 테스트는 검색 중복·구문 검색·브랜치 보호·빈 입력과 기본 명령을 확인합니다.
무작위 DAG 50개, 다중 부모 조상 탐색, 정렬 안정성, hash 충돌 재시도,
실제 REPL 실행 및 exit/quit 종료도 검증합니다.

## 명령 예시

```
mini-git> init "Alice"
Initialized repository.
Current branch: main
Current user: Alice

mini-git> commit "Initial commit"
[main a1b2c3] Initial commit

mini-git> branch feature
Created branch: feature

mini-git> switch feature
Switched to branch: feature

mini-git> commit "Add login feature"
[feature d4e5f6] Add login feature

mini-git> switch main
Switched to branch: main

mini-git> commit "Add payment feature"
[main g7h8i9] Add payment feature

mini-git> log
commit a1b2c3 (Alice, 2024-01-15 09:00:00) [main]
Initial commit
commit d4e5f6 (Alice, 2024-01-15 09:15:00) [feature]
Add login feature
commit g7h8i9 (Alice, 2024-01-15 09:30:00) [main]
Add payment feature

mini-git> path a1b2c3 g7h8i9
Path: a1b2c3 -> g7h8i9

mini-git> search login
Found 1 commit:

- d4e5f6: Add login feature
```

(실제 커밋 hash는 매 실행마다 SHA-1 기반으로 새로 생성되므로 위 예시와
다른 값이 나오는 것이 정상입니다.)

더 자세한 실행 로그와 알고리즘 설명은 같은 폴더의 `가이드.md`,
`평가질문_설명자료.md`, `제출/실행결과.md`를 참고하세요.

## 실행·검증·평가 발표 자료

VS Code 탐색기에서 `b3-2 → 제출 → 발표자료`를 펼치면 발표 파일을 볼 수 있습니다.

- [PowerPoint 발표 자료](제출/발표자료/MiniGit_실행검증_평가설명.pptx): 26장, 편집 가능한 도형·텍스트와 발표자 노트
- [PDF 읽기 자료](제출/발표자료/MiniGit_실행검증_평가설명.pdf)
- [발표자 설명 노트](제출/발표자료/발표자_설명노트.txt)
- [사용 안내](제출/발표자료/사용안내.txt)

같은 폴더에 미리보기 이미지, 콘텐츠 원본, 재생성 스크립트와 검증 기록도 있습니다.
