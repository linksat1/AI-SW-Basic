# 보너스: report.sh + log_archive.sh 증거

## 보너스 1: report.sh

### 파일 정보
```
경로: /home/agent-admin/agent-app/bin/report.sh
소유자: agent-dev:agent-core  권한: 750
```

### 실행 결과 (전체 로그 77 samples 분석)
```
분석 범위: 전체 로그

    ====== STATISTICS REPORT ======
      [CPU]
        Average : 0.1%
        Maximum : 1.1% at 2026-05-24 20:33:01
        Minimum : 0.0% at 2026-05-24 19:05:55
      [Memory]
        Average : 4.7%
        Maximum : 5.2% at 2026-05-24 20:52:01
        Minimum : 2.6% at 2026-05-26 20:51:49
      [Disk]
        Average : 1.0%
        Maximum : 1.0% at 2026-05-24 19:05:55
        Minimum : 1.0% at 2026-05-24 19:05:55
      [Samples]
        Data Points: 77 samples
```

### 시간 범위 지정 사용법
```bash
# 전체 로그 분석
/home/agent-admin/agent-app/bin/report.sh

# 시간 범위 지정
/home/agent-admin/agent-app/bin/report.sh "2026-05-26 20:00:00" "2026-05-26 21:00:00"
```

---

## 보너스 2: log_archive.sh

### 파일 정보
```
경로: /home/agent-admin/agent-app/bin/log_archive.sh
소유자: agent-admin:agent-core  권한: 750
```

### 실행 결과
```
[INFO] 7일 경과 로그 파일 압축 중...
[INFO] 압축 대상 없음 (7일 이내 로그만 존재)
[INFO] 30일 경과 아카이브 파일 삭제 중...
[INFO] 삭제 대상 없음 (30일 이내 아카이브만 존재)
[INFO] 로그 보존 정책 완료
```

### 정책
| 대상 | 조건 | 처리 |
|------|------|------|
| /var/log/agent-app/*.log | 7일 이상 경과 | 압축(.gz) 후 archive 이동 |
| /var/log/monitor/agent-app/archive/*.gz | 30일 이상 경과 | 삭제 |

### 예외 처리
- 아카이브 디렉토리 미존재 → 자동 생성 (실패 시 exit 1)
- 로그 디렉토리 미존재 → exit 1
- 압축 대상 0개 → [INFO] 메시지 후 정상 종료
- 압축 실패 → [WARNING] 출력 후 계속 진행

### crontab 등록 (선택)
```
0 2 * * * /home/agent-admin/agent-app/bin/log_archive.sh >> /var/log/agent-app/archive.log 2>&1
```
