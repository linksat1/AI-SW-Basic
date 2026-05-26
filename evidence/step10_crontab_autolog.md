# 9~10단계: sudoers NOPASSWD + crontab 자동 실행 증거

## [9단계] sudoers NOPASSWD

### /etc/sudoers.d/agent-admin 내용
```
agent-admin ALL=(ALL) NOPASSWD: /usr/sbin/ufw status, /usr/sbin/ufw *
```
- ✅ 문법 검증 완료 (visudo -c)
- ✅ agent-admin이 패스워드 없이 ufw 명령 실행 가능

---

## [10단계] crontab 자동 실행

### agent-admin crontab 등록 내용
```
* * * * * /home/agent-admin/agent-app/bin/monitor.sh >> /var/log/agent-app/monitor_cron.log 2>&1
```

### cron 실행 이력 (/var/log/syslog)
```
May 26 20:49:01 b1-lab CRON[1541]: (agent-admin) CMD (/home/agent-admin/agent-app/bin/monitor.sh >> /var/log/agent-app/monitor_cron.log 2>&1)
May 26 20:50:01 b1-lab CRON[1557]: (agent-admin) CMD (/home/agent-admin/agent-app/bin/monitor.sh >> /var/log/agent-app/monitor_cron.log 2>&1)
May 26 20:51:01 b1-lab CRON[1577]: (agent-admin) CMD (/home/agent-admin/agent-app/bin/monitor.sh >> /var/log/agent-app/monitor_cron.log 2>&1)
May 26 20:52:01 b1-lab CRON[1682]: (agent-admin) CMD (/home/agent-admin/agent-app/bin/monitor.sh >> /var/log/agent-app/monitor_cron.log 2>&1)
May 26 20:53:01 b1-lab CRON[1722]: (agent-admin) CMD (/home/agent-admin/agent-app/bin/monitor.sh >> /var/log/agent-app/monitor_cron.log 2>&1)
```

### monitor.log 누적 확인
```
[2026-05-26 20:51:01] PID:1570 CPU:0.0% MEM:4.2% DISK_USED:1%
[2026-05-26 20:51:49] PID:1570 CPU:0.0% MEM:2.6% DISK_USED:1%
[2026-05-26 20:52:01] PID:1570 CPU:0.0% MEM:3.1% DISK_USED:1%
[2026-05-26 20:53:01] PID:1570 CPU:0.0% MEM:3.4% DISK_USED:1%
```

## 검증 결과
- ✅ cron 서비스 active 상태
- ✅ agent-admin crontab 매분(*) 실행 등록
- ✅ syslog에서 매분 CRON 실행 이력 확인
- ✅ monitor.log 매분 1줄씩 자동 누적
- ✅ 로그 포맷: [YYYY-MM-DD HH:MM:SS] PID:N CPU:X% MEM:X% DISK_USED:X%
