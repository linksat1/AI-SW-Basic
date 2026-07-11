# 파일 기반 가계부 콘솔 프로그램 (budget_app)

Python 표준 라이브러리만으로 만든 CLI 가계부 프로그램입니다. 수입/지출 내역을 파일에
영구 저장하고, 조회/검색/월별 요약/예산/카테고리 관리/CSV 가져오기·내보내기를 지원합니다.

## 실행 방법

Python 3.10 이상이 필요합니다. `budget_app` 폴더의 **부모 폴더**(이 저장소 기준 `b2-1/`)에서
실행해야 `python -m budget_app`이 패키지를 찾을 수 있습니다.

```bash
cd b2-1
python3 -m budget_app --help
```

기본 데이터 저장 폴더는 실행한 위치 기준 `./data`입니다. `--data-dir` 옵션으로 바꿀 수 있습니다.

```bash
python3 -m budget_app --data-dir ./my_data add
```

## 저장 파일 위치 / 형식

저장 형식은 **JSONL**(한 줄에 JSON 객체 하나)이며, 3개 파일로 분리 저장합니다.

| 파일 | 내용 |
|---|---|
| `data/transactions.jsonl` | 거래 내역 (id, date, type, category, amount, memo, tags) |
| `data/categories.jsonl` | 카테고리 목록 |
| `data/budgets.jsonl` | 월별 예산 (month, amount) |

파일이 없으면 명령 실행 시 자동 생성됩니다. `categories.jsonl`이 비어 있으면
기본 카테고리(`food, transport, rent, salary, etc`)가 자동으로 채워집니다.

수정(`update`)/삭제(`delete`)/카테고리 변경 시에는 임시 파일에 새 내용을 모두 쓴 뒤
`os.replace`로 원자적으로 교체합니다. 그래서 쓰는 도중 프로그램이 강제 종료되어도
원본 파일이 절반만 쓰인 상태로 깨지지 않습니다.

> **"최신순"의 기준**: `list`/`search`는 파일에 저장된 순서(= 입력한 순서)의 역순으로
> "최신순"을 정의합니다. 대용량 파일이라도 정렬을 위해 전체를 메모리에 올리지 않고,
> 제너레이터로 한 줄씩 읽으면서 처리하기 위한 설계입니다.

## 주요 명령 예시

```bash
# 거래 추가 (대화형 입력)
python3 -m budget_app add

# 최근 10건 조회
python3 -m budget_app list --limit 10

# 조건 검색
python3 -m budget_app search --category food --from 2024-01-01 --to 2024-01-31

# 월별 요약 (지출 TOP 3)
python3 -m budget_app summary --month 2024-01 --top 3

# 월 예산 설정
python3 -m budget_app budget set --month 2024-01 --amount 500000

# 카테고리 관리 (대화형)
python3 -m budget_app category add
python3 -m budget_app category list
python3 -m budget_app category remove

# 거래 수정 (옵션 기반으로 고정)
python3 -m budget_app update --id TX-000001 --amount 18000 --memo "점심(수정)"

# 거래 삭제
python3 -m budget_app delete --id TX-000001

# CSV 내보내기 / 가져오기
python3 -m budget_app export --out export.csv --month 2024-01
python3 -m budget_app import --from import.csv
```

모든 명령은 `--help`로 사용법을 확인할 수 있습니다. 예: `python3 -m budget_app search --help`

### `update` 명령 방식 고정 안내

`update`는 과제 요구사항의 "(안 A) 옵션 기반"으로 고정했습니다.

```
update --id <id> [--date ...] [--type ...] [--category ...] [--amount ...] [--memo ...] [--tags ...]
```

지정한 옵션만 골라서 수정되고, 지정하지 않은 필드는 기존 값이 유지됩니다.

### `category add` / `category remove`는 대화형

예산·거래와 달리 카테고리 추가/삭제는 이름을 대화형으로 입력받습니다
(`카테고리명: ` / `삭제할 카테고리명: ` 프롬프트).

## import / export CSV 스키마

| column | required | 설명 |
|---|---|---|
| date | Y | YYYY-MM-DD |
| type | Y | income / expense |
| category | Y | 등록된 카테고리 |
| amount | Y | 양수 정수 |
| memo | N | 문자열 |
| tags | N | 쉼표(,)로 구분한 문자열 |

인코딩은 UTF-8, 첫 줄은 헤더를 포함합니다. `import`는 한 줄씩 검증하며,
검증에 실패한 행은 건너뛰고 마지막에 `imported=성공건수, skipped=실패건수`를 출력합니다.
`export`는 `--month` 또는 `--from`/`--to` 조건 중 최소 1개가 있어야 실행됩니다.

## 코드 구조 (모듈 분리)

```
budget_app/
├── __main__.py     ← `python -m budget_app` 진입점
├── cli.py          ← 인자 파싱(argparse), 대화형 입력, 화면 출력
├── service.py       ← 검증 + 비즈니스 로직 (BudgetService)
├── repository.py    ← 파일 I/O (TransactionRepository / CategoryStore / BudgetStore)
├── models.py         ← 데이터 모델 (Transaction dataclass)
├── decorators.py     ← 공통 관심사 분리 (예외 처리 / 실행 로그+시간 측정)
└── errors.py         ← 사용자 오류를 표현하는 AppError
```

각 계층의 책임:
- **cli.py**: 사용자와의 입출력만 담당. 검증/저장 로직은 직접 하지 않고 service를 호출.
- **service.py**: 날짜/금액/타입/카테고리 검증, 예산 계산, CSV 변환 등 규칙을 담당.
- **repository.py**: JSONL 파일을 어떻게 읽고 쓰는지만 담당(제너레이터 스트리밍, 원자적 쓰기).
- **models.py**: `Transaction` dataclass로 거래 1건의 구조를 정의.
- **decorators.py** / **errors.py**: 로그·시간측정·예외 처리라는 "공통 관심사"를 비즈니스 로직에서 분리.

## 예외 처리 및 종료 코드

- 예상 가능한 오류(잘못된 입력, 존재하지 않는 id 등)는 `AppError`로 표현하고,
  `[오류] 원인` + `[힌트] 해결 방법` 형태로만 출력합니다. 스택트레이스는 노출하지 않습니다.
- 정상 종료는 exit code `0`, 오류 종료는 `1`입니다.
- 모든 명령 실행은 `budget_app.log`(실행한 위치 기준)에 함수명/성공-실패/소요 시간이 기록됩니다.

## 개발 환경 / 제약

- Python 3.10 이상, 표준 라이브러리만 사용 (`argparse`, `dataclasses`, `csv`, `json`, `pathlib` 등)
- 옵션 표기는 `--` 통일 (`--limit`, `--from`, `--to`, `--month` 등)
