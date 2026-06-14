# Reports

이 폴더에는 최종 제출용 GitHub Issue 형식 리포트를 작성합니다.

권장 파일:

```text
oom.md
cpu-spike.md
deadlock.md
scheduling-analysis.md  # 선택 보너스
```

작성 방법:

```bash
cp ../templates/github-issue-template.md oom.md
cp ../templates/github-issue-template.md cpu-spike.md
cp ../templates/github-issue-template.md deadlock.md
cp ../templates/scheduling-analysis-template.md scheduling-analysis.md
```

각 파일에서 `{장애 유형}`, `{한 줄 요약}`과 빈 항목을 실제 실습 결과로 채우면 됩니다.

원본 `agent-leak-app`에서 미션 설명과 같은 결과가 나오지 않으면 아래처럼 제목을 잡아도 됩니다.

```text
[Bug] 원본 agent-leak-app에서 MEMORY_LIMIT 초과 후 MemoryGuard가 발동하지 않음
[Bug] 원본 agent-leak-app에서 CPU_MAX_OCCUPY 초과 후 Watchdog이 발동하지 않음
[Bug] 원본 agent-leak-app에서 MULTI_THREAD_ENABLE=true에도 Deadlock이 재현되지 않음
```

이 경우에도 원본 앱 실행 로그와 `ps`, `top`, `/proc/<PID>/status` 결과를 증거로 사용합니다.
