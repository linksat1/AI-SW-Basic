# Mini Git

커밋 그래프(DAG) / 위상 정렬 / 최단 경로(BFS) / 역색인 / 직접 구현한 병합
정렬로 만든 **CLI 기반 미니 버전 관리 시스템**입니다. 그래프 전용 라이브러리와
`sorted()`/`list.sort()` 같은 정렬 표준 API는 사용하지 않았습니다.

## 실행 방법

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
    └── index.py             역색인 (keyword/author -> commit hash 목록)
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

더 자세한 실행 로그와 알고리즘 설명은 상위 폴더의 `가이드.md`,
`평가질문_설명자료.md`, `제출/실행결과.md`를 참고하세요.
