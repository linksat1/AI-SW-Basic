# Evidence

이 폴더에는 실습 중 수집한 증거를 저장합니다.

B1-1 환경을 그대로 사용할 경우 원본 로그는 보통 `/var/log/agent-app`에 먼저 쌓입니다. 제출 전 필요한 로그를 이 폴더의 `logs/` 아래로 복사해 정리하면 됩니다.

권장 구조:

```text
evidence/
├── README.md
└── logs/
    ├── oom_before_app.log
    ├── oom_before_monitor.log
    ├── oom_after_app.log
    ├── oom_after_monitor.log
    ├── cpu_before_app.log
    ├── cpu_before_monitor.log
    ├── cpu_after_app.log
    ├── cpu_after_monitor.log
    ├── deadlock_before_app.log
    ├── deadlock_before_monitor.log
    ├── deadlock_after_app.log
    └── deadlock_after_monitor.log
```

로그가 너무 길면 리포트에는 핵심 구간만 발췌하고, 원본 로그는 이 폴더에 보관합니다.
