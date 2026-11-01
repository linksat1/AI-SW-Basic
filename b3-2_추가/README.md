# AI 코드 설명 자동 생성 도우미

Git 변경 사항(`git status`, `git diff`)과 작성자의 수정 의도를 AI API(Anthropic Claude)에 전달해,
리뷰·발표에 바로 쓸 수 있는 **코드 설명 초안**(제목 1줄 + 4개 섹션 본문)을 터미널에 출력하는 Python CLI입니다.

```
Git 수집 → 수정 의도 입력 → (safe-mode 마스킹/전송 제한) → 프롬프트 구성
→ AI API 호출(1회, 형식 오류 시 최대 2회) → 파싱·정리 → 형식 검증 → (후처리 보정) → 출력
```

## 구성

| 파일 | 역할 |
|---|---|
| `main.py` | 엔트리 포인트 |
| `ai_code_desc/cli.py` | `describe` 명령 흐름, CLI 옵션, 재생성 정책(최대 2회 호출) |
| `ai_code_desc/git_context.py` | 저장소 루트 확인, `git status`/`git diff` 수집(unstaged + staged + 새 파일) |
| `ai_code_desc/safe_mode.py` | 민감정보 정규식 마스킹, 파일/줄 수 전송 제한 |
| `ai_code_desc/ai_client.py` | Messages API 호출, 오류 원인별 메시지 |
| `ai_code_desc/generator.py` | 프롬프트, 응답 파싱, 형식 정리·검증·후처리, 출력 |
| `ai_code_desc/convention.py` | 팀 컨벤션 파일 로딩 |
| `conventions/ai-sw-basic.json` | 이 저장소 커밋 스타일을 분석한 팀 컨벤션 예시 |
| `tests/test_ai_code_desc.py` | 자동 테스트 27개 |
| `제출/` | 실행 결과 증빙과 보너스 과제 자료 |

## 1. 설치

Python 3.10 이상이 필요합니다.

```bash
cd b3-2_추가
python3 -m venv .venv && source .venv/bin/activate   # 선택
python3 -m pip install -r requirements.txt            # anthropic>=2.3.0
```

`--mock`과 `--dry-run`은 표준 라이브러리만 사용하므로 패키지를 설치하지 않아도 동작합니다.

## 2. 환경변수(API Key) 설정

API Key는 **환경변수로만** 읽습니다. 코드와 설정 파일에는 키를 적지 않습니다.

```bash
export AI_API_KEY="YOUR_KEY"          # 우선 사용
# 또는 export ANTHROPIC_API_KEY="YOUR_KEY"
```

셸 기록에 키가 남지 않게 하려면 `read -s AI_API_KEY && export AI_API_KEY`처럼 입력하세요.
`.env` 파일을 쓴다면 `.gitignore`에 포함되어 있으므로 커밋되지 않습니다.

## 3. 실행 방법

**Git 저장소의 루트 디렉터리에서** 실행합니다. 하위 폴더에서 실행하면 루트 경로를 알려주고 종료합니다.

```bash
# 저장소 루트가 b3-2_추가의 상위(AI-SW-Basic)인 경우
cd /path/to/AI-SW-Basic
python3 b3-2_추가/main.py describe                       # 수정 의도를 대화식으로 입력
python3 b3-2_추가/main.py describe --intent "로그인 로직을 수정했고, 세션 처리와 예외 처리를 보완했다."
```

### 자주 쓰는 명령

```bash
python3 main.py describe --mock --intent "..."          # API 없이 전체 흐름 확인 (호출 0회)
python3 main.py describe --dry-run --safe-mode          # AI로 보낼 프롬프트만 확인 (호출 0회)
python3 main.py describe --safe-mode --intent "..."     # 권장: 마스킹 + 전송 제한 후 호출
python3 main.py describe --model claude-sonnet-5-5 --effort medium --max-tokens 8000
python3 main.py describe --convention conventions/ai-sw-basic.json
python3 main.py --version
```

### 옵션

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `--intent`, `-i` | (대화식 입력) | 수정 의도/요약. 생략하면 프롬프트에서 입력받고, `--no-input`이면 건너뜀 |
| `--model` | `claude-opus-5-5` | 모델 ID |
| `--max-tokens` | `16000` | 응답 최대 토큰. 모델의 사고(thinking) 토큰도 포함되므로 너무 낮추면 응답이 잘림 |
| `--effort` | `low` | `low`/`medium`/`high`/`xhigh`/`max`. 높을수록 더 깊이 분석하지만 토큰·시간 증가 |
| `--temperature` | (보내지 않음) | 지정하면 그대로 전송. 아래 참고 |
| `--safe-mode` | 꺼짐 | 민감정보 마스킹 + 전송량 제한 |
| `--max-files` / `--max-diff-lines` | `10` / `200` | safe-mode 전송 한도 |
| `--mask-pattern REGEX` | - | safe-mode 추가 마스킹 정규식(여러 번 지정 가능) |
| `--convention PATH` | 루트의 `.ai-code-summary.json` | 팀 컨벤션 파일 |
| `--mock` | - | API 대신 데모 응답 사용 |
| `--dry-run` | - | 프롬프트만 출력하고 종료 |

> **temperature 안내**: 현재 Anthropic API 버전(2026-10-21)과 기본 모델 `claude-opus-5-5`는 `temperature`를
> 받지 않고 400 오류를 반환합니다. 그래서 기본값은 "보내지 않음"이고, 결과의 일관성과 깊이는 `--effort`로 조절합니다.
> `--temperature`를 지정하면 요청에 포함하며, 400 응답이 오면 원인과 함께 옵션을 빼라는 안내를 출력합니다.

## 4. 출력 예시

```text
$ python3 main.py describe --intent "로그인 세션 처리를 수정했고, 세션 검증과 예외 처리를 보완했다."
[INFO] Git status 수집 완료: 2개 파일 변경 감지
[INFO] Git diff 수집 완료: 41줄
[INFO] 컨벤션: 기본 컨벤션 (Conventional Commits) (내장 기본값)
[INFO] 사용자 입력 수집 완료: 수정 의도 36자
[INFO] safe-mode OFF: diff 전체를 전송합니다.
[INFO] AI API 요청 중... (model=claude-opus-5-5, effort=low, max_tokens=16000, 1회차)
[DONE] 코드 설명 생성 완료

--- Description Title --- (24자)
feat: 세션 검증과 예외 처리 구조 보완

--- Description Body ---
## Summary
- 빈 사용자 입력과 비활성 세션을 SessionError로 명확히 거부합니다.

## What Changed
- `session.py`: create_session()에 빈 입력 검증을, validate_session()을 새로 추가했습니다.
- `session.py`: 세션 실패 전용 예외 SessionError를 정의했습니다.

## Why It Was Needed
- 이전에는 빈 사용자명으로도 세션이 만들어져 상태가 일관되지 않았습니다.

## How to Verify
- `create_session("")`이 SessionError를 내는지 확인합니다.
- 비활성 세션으로 `validate_session()`을 호출해 예외 경로를 확인합니다.
----------------------

--- Validation ---
[OK] 제목 길이/섹션 헤더/섹션별 불릿 검증 통과
[INFO] safe-mode OFF
[INFO] AI API 호출 횟수: 1회 (최대 2회)
[NOTE] 생성된 설명은 초안입니다. 내용을 검토한 뒤 적용하세요.
```

위 본문은 형식을 보여주기 위한 예시입니다. 실제 문장은 변경 내용과 모델 응답에 따라 달라집니다.

### 오류 상황 출력

```text
# 변경 사항 없음
[INFO] 변경 사항이 없습니다. 코드 설명을 생성하지 않고 종료합니다.

# API Key 미설정
[ERROR] AI_API_KEY 환경변수가 설정되지 않았습니다.
## 예) export AI_API_KEY="YOUR_KEY"

# 잘못된 API Key (실제 호출 결과)
[ERROR] 인증 실패(401): API Key가 올바른지 확인하세요. (invalid x-api-key)
[INFO] AI API 호출 횟수: 1회
```

이 밖에 403(권한), 404(모델 ID 오류), 429(요청 한도), 5xx(서버 오류), 시간 초과, 네트워크 연결 실패,
모델 거절(refusal)을 각각 다른 메시지로 안내합니다.

## 5. 설명 템플릿과 형식 검증

| 규칙 | 기준 | 위반 시 |
|---|---|---|
| 제목 | 1줄, 50자 이내 권장, 최대 72자 | 72자 초과는 오류, 50자 초과는 경고 |
| 본문 섹션 | `Summary`, `What Changed`, `Why It Was Needed`, `How to Verify` | 누락은 오류 |
| 섹션 불릿 | 각 섹션 `- ` 불릿 1개 이상(권장 최대 3개) | 0개는 오류, 초과는 경고 |
| 컨벤션 접두어 | `feat`, `fix` 등 | 경고 |

처리 순서:

1. **정리**: 코드블록 감싸기, `### Summary`/`**Summary**`, `*` 불릿 같은 표기를 표준 형식으로 바꿉니다(내용은 바꾸지 않음).
2. **검증 후 재생성**: 오류가 있으면 오류 목록을 프롬프트에 넣어 **1회만** 다시 요청합니다(총 2회까지).
3. **후처리 보정**: 그래도 남은 오류는 제목을 72자로 자르고, 빠진 섹션에 "검토 후 직접 작성" 불릿을 넣어 보정합니다.

## 6. 민감정보 대응 (safe-mode)

`git diff`에는 API Key, 비밀번호, 개인정보가 섞여 있을 수 있습니다. `--safe-mode`는 전송 전에 다음을 적용합니다.

| 정책 | 기본 기준 | 조정 방법 |
|---|---|---|
| (A) 마스킹 | Anthropic/OpenAI 형식 키, AWS Access Key, GitHub/Slack 토큰, 개인키 헤더, `password=`/`token:` 같은 대입문, 이메일, 휴대폰 번호 | `--mask-pattern REGEX`, 컨벤션 `safe_mode.extra_mask_patterns` |
| (B) 파일 수 제한 | 최대 **10개 파일** | `--max-files N`, 컨벤션 `safe_mode.max_files` |
| (B) 줄 수 제한 | 최대 **200줄** | `--max-diff-lines N`, 컨벤션 `safe_mode.max_lines` |

safe-mode를 켜고 끈 결과는 [제출/results/06_safe-mode_OFF_ON_비교.txt](제출/results/06_safe-mode_OFF_ON_비교.txt)에 있습니다.
`--dry-run --safe-mode`로 AI에 실제로 전달될 내용을 먼저 확인하는 것을 권장합니다.

- 마스킹은 알려진 패턴만 잡습니다. 사내 식별번호처럼 형식이 정해진 값은 `--mask-pattern`으로 추가하세요.
- 수정 의도(`--intent`)와 파일 이름은 마스킹하지 않으므로 민감정보를 적지 마세요.
- 전송 제한을 쓰면 잘린 파일은 설명에 반영되지 않습니다. 프롬프트 끝에 생략 사실이 표시됩니다.
- 파일은 `git diff` 출력 순서(경로순)로 잘리므로 문서 파일이 앞에 오면 핵심 코드가 빠질 수 있습니다. 큰 변경은 `--max-files`를 늘리거나 변경을 나눠 실행하세요.

## 7. 비용·요청 횟수와 권장 사용법

- `describe` 1회 실행은 AI API를 **1회** 호출하고, 형식 검증 실패 시에만 **최대 2회**까지 호출합니다. 호출 횟수는 매번 출력됩니다.
- SDK는 일시적 오류(429, 5xx, 연결 오류)에 한해 같은 요청을 최대 2번 자동 재시도합니다.
- 비용은 입력(diff 길이)과 출력 토큰에 비례합니다. 큰 변경은 `--safe-mode`로 전송량을 줄이고, 변경을 작은 단위로 나눠 실행하세요.
- 기본 `--effort low`는 요약 작업에 충분합니다. 결과가 얕을 때만 `medium`/`high`로 올리세요.
- 형식 확인이나 시연은 `--mock`/`--dry-run`으로 하면 비용이 들지 않습니다.
- 생성된 설명은 초안입니다. 사실과 다른 부분이 없는지 검토한 뒤 적용하세요.
- 도구는 `git push`, PR 생성 같은 원격 반영을 하지 않습니다.

## 8. 팀 컨벤션 (설명 템플릿 커스터마이징)

이전 미션들의 커밋 기록(92개)을 분석한 결과, 이 저장소는 `Add/Update/Improve/Move` 같은 **영어 명령형 동사**로
제목을 시작하고 `B2-1`, `Mini Git`처럼 **과제 코드나 프로젝트 이름**을 넣는 스타일을 씁니다(`docs:` 접두어도 일부 사용).
이를 [conventions/ai-sw-basic.json](conventions/ai-sw-basic.json)으로 정의했습니다.

| 항목 | 기본 컨벤션 | AI-SW-Basic 팀 컨벤션 |
|---|---|---|
| 제목 접두어 | `feat`, `fix`, `refactor`, `docs`, `test`, `chore` | `Add`, `Update`, `Improve`, `Fix`, `Move`, `Remove`, `Organize`, `docs` |
| 제목 형식 | `<type>: <한국어 요약>` | 영어 명령형 동사 + 대상 + 과제 코드 |
| 본문 | 한국어 | 한국어, What Changed는 `파일 경로: 변경 내용` |
| 추가 규칙 | - | 검증 명령은 백틱, 증빙 파일 변경 시 평가 항목과의 관계를 적음 |
| safe-mode 추가 패턴 | - | 주민등록번호 형식 |

적용 방법(둘 중 하나):

```bash
python3 main.py describe --convention conventions/ai-sw-basic.json
cp conventions/ai-sw-basic.json <저장소 루트>/.ai-code-summary.json   # 자동 적용
```

컨벤션 규칙은 프롬프트의 "작성 규칙"에 들어가고, 제목 접두어와 길이 검증에도 쓰입니다.
적용 전/후 비교는 [제출/results/07_컨벤션_적용전후_비교.txt](제출/results/07_컨벤션_적용전후_비교.txt)에 있습니다.

## 9. 테스트

```bash
python3 -B -m unittest discover -s tests -v
```

임시 Git 저장소를 만들어 수집, safe-mode, 형식 검증·재생성·보정, 컨벤션, CLI 흐름, SDK 오류 변환을 검사합니다.
실제 API는 호출하지 않습니다. SDK 오류 변환 테스트 3개는 `anthropic` 패키지가 설치되어 있을 때만 실행됩니다.
제출 증빙은 `bash 제출/make_results.sh`로 다시 만들 수 있습니다.

## 10. GitHub 저장소

이 프로젝트는 [linksat1/AI-SW-Basic](https://github.com/linksat1/AI-SW-Basic) 저장소의 `b3-2_추가/` 폴더에 있습니다.
도구 자체는 원격 저장소에 아무것도 반영하지 않으며, push는 사용자가 직접 수행합니다.
