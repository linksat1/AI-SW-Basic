#!/bin/zsh
# B4_평가자_답변.pdf의 실행 근거를 순서대로 재현하는 명령 모음.
#
# 사용법 (b2-1 폴더에서):
#   한 줄씩 복사해서 실행하거나, 전체 실행:  zsh 평가/B4a_시연_명령어.sh
#
# - 모든 명령은 빈 demo 폴더를 사용합니다 (실제 data/ 폴더는 건드리지 않음).
# - --data-dir는 반드시 명령 이름 뒤에 둡니다.
# - 시연 후 정리:  rm -r demo imp.csv out.csv

if [ -e demo ]; then
  echo "demo 폴더가 이미 있습니다. 새로 시작하려면 먼저 rm -r demo 를 실행하세요."
  exit 1
fi

# ── 시연 준비 (PDF 2쪽) ──────────────────────────────────────────
cat > imp.csv <<'EOF'
date,type,category,amount,memo,tags
2024-01-20,expense,transport,1250,지하철,
2024-01-21,expense,없는카테고리,1000,깨짐,
2024-01-22,income,salary,50000,보너스,
EOF
cat imp.csv

# ── 항목 1-1 (1/2) add · list · search (PDF 3쪽) ─────────────────
# add는 대화형입니다. 직접 입력하려면: python3 -m budget_app add --data-dir demo
printf '2024-01-15\nexpense\nfood\n15000\n점심\nmeal\n' | python3 -m budget_app add --data-dir demo
printf '2024-01-25\nincome\nsalary\n3000000\n월급\n\n' | python3 -m budget_app add --data-dir demo
python3 -m budget_app list --data-dir demo
python3 -m budget_app search --category food --data-dir demo

# ── 항목 1-1 (2/2) summary · update · import · export · delete (PDF 4쪽)
python3 -m budget_app budget set --month 2024-01 --amount 100000 --data-dir demo
python3 -m budget_app summary --month 2024-01 --data-dir demo
python3 -m budget_app update --id TX-000001 --amount 18000 --data-dir demo
python3 -m budget_app import --from imp.csv --data-dir demo
python3 -m budget_app export --out out.csv --month 2024-01 --data-dir demo
python3 -m budget_app delete --id TX-000002 --data-dir demo

# ── 항목 1-2 재실행 후 데이터 유지 (PDF 5쪽) ─────────────────────
printf 'hobby\n' | python3 -m budget_app category add --data-dir demo
ls demo
python3 -m budget_app list --data-dir demo
python3 -m budget_app category list --data-dir demo
cat demo/budgets.jsonl

# ── 항목 1-3 사용 중 카테고리 삭제 거부 (PDF 6쪽) ─────────────────
printf 'food\n' | python3 -m budget_app category remove --data-dir demo
echo "종료 코드: $?"
printf 'hobby\n' | python3 -m budget_app category remove --data-dir demo

# ── 항목 1-4 예산 사용률·초과 경고 (PDF 7쪽) ─────────────────────
python3 -m budget_app budget set --month 2024-01 --amount 10000 --data-dir demo
cat demo/budgets.jsonl
python3 -m budget_app summary --month 2024-01 --data-dir demo

# ── 항목 1-5 CSV 스키마 (PDF 8쪽) ────────────────────────────────
cat imp.csv
cat out.csv

# ── 항목 1-6·7 오류 메시지와 종료 코드 (PDF 9쪽) ──────────────────
python3 -m budget_app update --id TX-999999 --amount 1000 --data-dir demo
echo "종료 코드: $?"
python3 -m budget_app export --out x.csv --data-dir demo
echo "종료 코드: $?"
python3 -m budget_app import --from nofile.csv --data-dir demo
echo "종료 코드: $?"
python3 -m budget_app summary --month 2024-13 --data-dir demo
echo "종료 코드: $?"

# ── 항목 2-1 모듈 분리 (PDF 10쪽) ────────────────────────────────
ls budget_app/*.py
grep -n "^from budget_app" budget_app/*.py

# ── 항목 2-2 클래스 (PDF 11쪽) ───────────────────────────────────
grep -n "^class" budget_app/*.py

# ── 항목 2-3 update/delete 안전 처리 (PDF 12쪽) ──────────────────
python3 -m budget_app delete --id TX-000003 --data-dir demo
ls demo
python3 -m budget_app delete --id TX-999999 --data-dir demo

# ── 항목 3-1 제너레이터 (PDF 13쪽) ───────────────────────────────
python3 -c "from pathlib import Path; from budget_app.repository import TransactionRepository as R; g = R(Path('demo/transactions.jsonl')).iter_all(); print(type(g).__name__); print(next(g))"
python3 -m budget_app list --limit 1 --data-dir demo

# ── 항목 3-2 데코레이터 (PDF 14쪽) ───────────────────────────────
grep -c "^@handle_errors" budget_app/cli.py
tail -3 budget_app.log
python3 -c "from budget_app.cli import cmd_add; print(cmd_add.__name__)"

# ── 항목 3-3 타입 힌트 (PDF 15쪽) ────────────────────────────────
python3 -c "import typing; from budget_app.service import validate_amount, BudgetService; print(typing.get_type_hints(validate_amount)); print(typing.get_type_hints(BudgetService.search_transactions)['date_from'])"
# 금액 abc 입력 시 재입력 요청 확인은 직접 실행: python3 -m budget_app add --data-dir demo

# ── 항목 4-1 JSONL vs CSV (PDF 16쪽) ─────────────────────────────
head -1 demo/transactions.jsonl
sed -n 2p out.csv

# ── 항목 4-3 깨진 CSV 행 (PDF 18쪽) ──────────────────────────────
# imp.csv를 가져온 결과는 항목 1-1(2/2)의 import 출력: imported=2, skipped=1

# ── 항목 4-2 거래 10만 건 측정 (PDF 17쪽, 선택) ───────────────────
# 오래 걸리므로 기본으로는 실행하지 않습니다. 필요하면 아래 주석을 풀어 실행하세요.
# python3 -c "import json, random; random.seed(1); cats=['food','transport','rent','salary','etc']; import os; os.makedirs('bench', exist_ok=True); f=open('bench/transactions.jsonl','w'); [f.write(json.dumps({'id':f'TX-{i:06d}','date':f'2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}','type':'income' if (c:=random.choice(cats))=='salary' else 'expense','category':c,'amount':random.randint(1000,50000),'memo':'메모','tags':[]}, ensure_ascii=False)+'\n') for i in range(1,100001)]"
# /usr/bin/time -l python3 -m budget_app list --limit 5 --data-dir bench > /dev/null
# /usr/bin/time -l python3 -m budget_app update --id TX-050000 --amount 1 --data-dir bench > /dev/null
