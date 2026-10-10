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

자동 생성되는 `__pycache__/` 등 캐시 폴더는 생략했습니다.

```
b3-2/
├── .gitignore                         ← Git 추적 제외 설정
├── 과제                               ← 원본 과제 요구사항 (참고용, 수정 X)
├── main.py                            ← 엔트리 포인트 (필수 제출물 1)
├── mini_git/                          ← 실제 구현체
│   ├── __init__.py                      패키지 정의
│   ├── cli.py                           REPL, 명령어 파싱, 출력 포맷팅
│   ├── repository.py                    저장소 상태(브랜치/HEAD/사용자) 관리
│   ├── commit.py                        Commit 노드 + 세션 내 유일한 hash 생성
│   ├── traversal.py                     위상 정렬 / 최단 경로 / 조상 탐색
│   ├── sorting.py                       직접 구현한 병합 정렬
│   ├── index.py                         역색인
│   └── errors.py                        표준 에러 예외 클래스
├── tests/
│   └── test_mini_git.py                ← 자동 검증 테스트
├── 발표자료/
│   ├── 가이드.md                       ← 단계별 실행 가이드
│   ├── README.md                       ← 이 문서: 실행 방법, 명령어 목록 (필수 제출물 2)
│   ├── 평가질문_설명자료.md            ← 평가 질문 대비 설명 자료
│   ├── MiniGit_실행검증_평가설명.pptx  ← 발표 슬라이드
│   ├── MiniGit_실행검증_평가설명.pdf   ← 발표 슬라이드 PDF
│   ├── 전체슬라이드_미리보기.png       ← 슬라이드 전체 미리보기
│   ├── 발표자_설명노트.txt             ← 발표자 설명 노트
│   ├── 사용안내.txt                    ← 발표자료 사용 안내
│   ├── build_presentation.py           ← 발표자료 생성 스크립트
│   ├── deck_content.json               ← 슬라이드 구성 데이터
│   ├── 과제_재검증.txt                 ← 과제 재검증 기록
│   ├── 발표자료_검증결과.json          ← 발표자료 검증 결과
│   └── 최종검수결과.md                 ← 최종 검수 기록
└── 제출/
    ├── 실행결과.md                     ← 실행 결과 요약
    └── results/                        ← 시나리오별 원본 실행 로그
        ├── 01_저장소_브랜치_관리.txt
        ├── 02_LOG_위상정렬.txt
        ├── 03_LOG_정렬옵션.txt
        ├── 04_PATH_최단경로.txt
        ├── 05_ANCESTORS.txt
        ├── 06_SEARCH.txt
        ├── 07_에러처리_표준.txt
        ├── 08_대소문자무관_명령어.txt
        ├── 09_CLI_종료_quit.txt
        ├── 10_보완_회귀검증.txt
        └── 11_자동검증.txt
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
