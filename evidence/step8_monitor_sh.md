# 8단계: monitor.sh 작성 증거

## 파일 정보
```
경로: /home/agent-admin/agent-app/bin/monitor.sh
소유자: agent-dev
그룹: agent-core
권한: 750 (-rwxr-x---)
```

## ls -l 출력
```
-rwxr-x--- 1 agent-dev agent-core 4248 May 26 20:51 /home/agent-admin/agent-app/bin/monitor.sh
```

## 권한 해석
```
-rwxr-x---
 ├─rwx : agent-dev (소유자)  → 읽기+쓰기+실행 ✅
 ├─r-x : agent-core (그룹)   → 읽기+실행     ✅ (agent-admin 소속)
 └─--- : 기타                → 접근 불가     ✅
```

## 실행 결과 (agent-admin으로 실행)
```
====== SYSTEM MONITOR RESULT ======

[HEALTH CHECK]
Checking process 'agent-app-linux-x86'... [OK] (PID: 1570)
Checking port 15034... [OK]

[FIREWALL CHECK]
Firewall (UFW)... [OK] Active

[RESOURCE MONITORING]
CPU Usage  : 0.0%
MEM Usage  : 2.6%
DISK Used  : 1%

====================================
[INFO] Log appended: /var/log/agent-app/monitor.log
```

## 주요 구현 포인트
| 기능 | 구현 방식 |
|------|----------|
| 프로세스 확인 | `pgrep -f agent-app-linux-x86` → 없으면 exit 1 |
| 포트 확인 | `ss -tulnp \| grep :15034` → 없으면 exit 1 |
| 방화벽 확인 | `systemctl is-active ufw` (sudo 불필요, cron 호환) |
| CPU 수집 | `top -bn1 \| grep Cpu(s) \| awk` |
| MEM 수집 | `free \| grep Mem \| awk` |
| DISK 수집 | `df / \| tail -1 \| awk` |
| 로그 기록 | `echo [...] >> $LOG_FILE` (>> 누적, > 덮어쓰기 금지) |
| 로그 로테이션 | 10MB 초과 시 .1~.10 순환, 스크립트 자체 구현 |

## 검증 결과
- ✅ 소유자: agent-dev / 그룹: agent-core
- ✅ 권한: 750 (-rwxr-x---)
- ✅ agent-admin (agent-core 소속) 실행 가능
- ✅ 프로세스/포트 Health Check 동작
- ✅ 방화벽 상태 확인 (sudo 없이 가능)
- ✅ CPU/MEM/DISK 수집 및 임계값 경고
- ✅ /var/log/agent-app/monitor.log 누적 기록
