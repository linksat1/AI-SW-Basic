# B1-2 Codex 초보자 교본

이 폴더는 B1-2 미션인 **리눅스 프로세스 및 시스템 리소스 트러블슈팅**을 처음부터 따라 할 수 있도록 정리한 실습 교본입니다.

이 교본은 **원본 실행 파일 `agent-leak-app`을 사용하는 방식**으로 정리되어 있습니다.

환경은 B1-1에서 만든 기준을 그대로 이어 씁니다.

- 실행 계정: `agent-admin`
- 앱 홈: `/home/agent-admin/agent-app`
- 로그 디렉터리: `/var/log/agent-app`
- 포트: `15034`
- B1-2 앱 파일명: `agent-leak-app`

## 파일 구성

```text
b1-2_codex/
├── README.md
├── beginner-guide.md
├── scripts/
│   ├── monitor.sh
│   └── run_helpers.sh
├── templates/
│   ├── github-issue-template.md
│   └── scheduling-analysis-template.md
├── reports/
│   └── README.md
└── evidence/
    ├── README.md
    └── logs/
```

## 가장 먼저 볼 파일

1. [beginner-guide.md](beginner-guide.md)를 위에서부터 순서대로 따라 합니다.
2. 실습 중 원본 로그는 `/var/log/agent-app`에 저장하고, 제출용으로 정리한 로그는 `evidence/logs/`에 모읍니다.
3. 최종 보고서는 `templates/github-issue-template.md`를 복사해서 `reports/` 안에 3개로 작성합니다.

## 최종 제출물

- `reports/oom.md`
- `reports/cpu-spike.md`
- `reports/deadlock.md`
- 선택 보너스: `reports/scheduling-analysis.md`
- 각 보고서에서 참조하는 증거 로그 또는 스크린샷

원본 앱에서 미션 설명과 같은 종료/Deadlock 로그가 나오지 않는 경우에도, 그 차이를 `ps`, `top`, `/proc`, 로그 검색 결과로 증명해 리포트에 기록합니다.
