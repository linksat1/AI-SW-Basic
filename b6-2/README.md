# AI 기반 Git 커밋 & PR 자동 생성기

`git status`/`git diff` 결과를 Claude API에 전달해 커밋 메시지와 PR 제목/본문 초안을
자동으로 생성하는 Python CLI 도구입니다.

## 설치

```bash
cd b6-2
python3 -m pip install --user anthropic   # 유일한 외부 의존성: 공식 Anthropic SDK
```

## 환경변수(API 키) 설정

API 키는 코드에 하드코딩하지 않고 환경변수로만 전달합니다.

```bash
export AI_API_KEY="sk-ant-YOUR_KEY_HERE"
# 또는 (둘 중 하나만 있으면 됨)
export ANTHROPIC_API_KEY="sk-ant-YOUR_KEY_HERE"
```

키가 없는 상태로 실행하면 API를 호출하지 않고 즉시 아래 안내를 출력합니다.

```
오류: AI_API_KEY(또는 ANTHROPIC_API_KEY) 환경변수가 설정되지 않았습니다.
  export AI_API_KEY="YOUR_KEY"
위 명령으로 API 키를 설정한 뒤 다시 실행하세요.
```

## 실행 방법

```bash
# 변경사항을 스테이징한 뒤 커밋 메시지 생성
git add .
python main.py commit

# 옵션 지정
python main.py commit --model claude-opus-4-8 --max-tokens 512

# 민감정보 마스킹 + diff 크기 제한(safe-mode) 적용
python main.py commit --safe-mode

# PR 초안 생성 (기준 브랜치 지정, 없으면 origin/main)
python main.py pr --base origin/main
python main.py pr --base main --safe-mode
```

### 전체 옵션

| 옵션 | 적용 대상 | 기본값 | 설명 |
|---|---|---|---|
| `--model` | commit, pr | `claude-opus-4-8` | 사용할 Claude 모델 |
| `--temperature` | commit, pr | (미지정 시 요청에 미포함) | 샘플링 온도. 일부 최신 모델은 지원하지 않음 |
| `--max-tokens` | commit, pr | `1024` | 최대 출력 토큰 수 |
| `--safe-mode` | commit, pr | 꺼짐 | 민감정보 마스킹 + diff 크기 제한 적용 |
| `--max-diff-lines` | commit, pr | `400` | safe-mode에서 전송할 diff 최대 줄 수 |
| `--base` | pr | `origin/main` | PR diff 비교 기준 브랜치/커밋 |

## 출력 예시

`git add .` 후 `python main.py commit --safe-mode` 실행 시 (실제 AI 응답 예시 — 이 결과는
아래 "안전장치·비용 유의사항"에서 설명하는 이유로 이 환경에서는 mock 응답으로 파이프라인만
검증했습니다. 형식은 실제 실행 시와 동일합니다):

```
============================================================
커밋 메시지 초안
============================================================
[제목] (35자)
feat: add secret config placeholder

[본문]
Adds a config module for upcoming AWS integration.

------------------------------------------------------------
모델: claude-opus-4-8  |  max_tokens: 1024  |  temperature: None
safe-mode: ON  |  마스킹된 패턴: AWS Access Key x1, Anthropic API Key x1  |  diff 크기: 7줄 전체 전송
------------------------------------------------------------
✓ 길이/형식 검증 통과
============================================================
```

`python main.py pr --base origin/main --safe-mode` 실행 시:

```
============================================================
PR 초안
============================================================
[제목] (42자)
Add secret config module and health helper

[본문]
## Why
- Prepare configuration surface for upcoming AWS integration

## What
- Added secret_config.py placeholder
- Added add() helper function to app.py

## How to Test
- Run `python -c "import secret_config"` and confirm no import error

------------------------------------------------------------
모델: claude-opus-4-8  |  max_tokens: 1024  |  temperature: None
safe-mode: ON  |  마스킹된 패턴: AWS Access Key x1, Anthropic API Key x1  |  diff 크기: 7줄 전체 전송
------------------------------------------------------------
✓ 길이/형식 검증 통과
============================================================
```

전체 실행 캡처(총 10개 시나리오)는 [`제출/results/`](제출/results/), 정리된 설명은
[`제출/실행결과.md`](제출/실행결과.md)에 있습니다.

## 안전장치(safe-mode) 및 비용 유의사항

- **하드코딩 금지**: API 키는 소스 코드 어디에도 저장하지 않고 환경변수로만 읽습니다.
  로컬에서 `.env` 파일을 쓴다면 반드시 `.gitignore`에 추가해 실수로 커밋되지 않게 하세요.
- **safe-mode(`--safe-mode`)**: diff에 실수로 포함된 API 키/토큰/비밀번호 형태의 문자열을
  정규식으로 탐지해 마스킹한 뒤 전송하고, 전송하는 diff 크기도 기본 400줄로 제한합니다.
  민감한 저장소에서는 항상 `--safe-mode`를 켜는 것을 권장합니다.
- **비용**: 이 도구는 매 실행마다 최소 1회의 Claude API 호출을 발생시킵니다. `--max-tokens`를
  낮추면(커밋 메시지는 보통 512 이하로 충분) 응답 비용을 줄일 수 있고, `--safe-mode`의 diff
  크기 제한도 입력 토큰 비용을 함께 줄여줍니다. 대량의 커밋에 자동으로 돌리기 전에, 예상
  호출 빈도와 모델별 단가를 먼저 확인하세요.
- **temperature 미지원 모델**: `claude-opus-4-8` 등 최신 모델은 `temperature`를 비-기본값으로
  보내면 API가 요청 자체를 거부합니다. 이 도구는 `--temperature`를 지정하지 않으면 아예
  요청에 포함시키지 않아 이 문제를 피합니다. temperature를 실험해보고 싶다면 이를 지원하는
  이전 세대 모델(예: `claude-sonnet-4-6`)을 `--model`로 지정하세요.

## GitHub 저장소

`<여기에 실제로 push한 GitHub 저장소 URL을 기재하세요>`

## 소스 구조

```
b6-2/
├── main.py                진입점
├── ai_gitgen/
│   ├── git_utils.py       git status/diff 수집
│   ├── safe_mode.py        마스킹 + diff 크기 제한
│   ├── prompt_builder.py   AI 프롬프트 구성
│   ├── ai_client.py        Claude API 호출 + 예외 처리
│   ├── validators.py       응답 파싱 + 길이/형식 검증
│   ├── formatter.py         터미널 출력
│   ├── cli.py               argparse 서브커맨드 배선
│   └── errors.py             예외 클래스
├── 가이드.md                단계별 실행/설계 설명
├── 평가질문_설명자료.md      과제 목표 5개 항목별 답변
└── 제출/
    ├── 실행결과.md
    └── results/*.txt        10개 시나리오 실행 캡처
```

## 자세한 설계 설명

단계별 사용법과 설계 이유는 [`가이드.md`](가이드.md)를, 과제 목표 5개 항목에 대한 답변은
[`평가질문_설명자료.md`](평가질문_설명자료.md)를 참고하세요.
