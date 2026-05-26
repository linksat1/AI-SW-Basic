#!/bin/bash
# =============================================================
# report.sh - monitor.log 통계 분석 리포트
# 사용법: ./report.sh [시작시간] [종료시간]
# 예시:   ./report.sh "2026-05-26 10:00:00" "2026-05-26 11:00:00"
# =============================================================

LOG_FILE="/var/log/agent-app/monitor.log"
START_TIME="$1"
END_TIME="$2"

if [ ! -f "$LOG_FILE" ]; then
    echo "[ERROR] 로그 파일 없음: $LOG_FILE"
    exit 1
fi

if [ -n "$START_TIME" ] && [ -n "$END_TIME" ]; then
    LOG_DATA=$(awk -v s="[$START_TIME" -v e="[$END_TIME" '$0 >= s && $0 <= e' "$LOG_FILE")
    echo "분석 범위: $START_TIME ~ $END_TIME"
else
    LOG_DATA=$(cat "$LOG_FILE")
    echo "분석 범위: 전체 로그"
fi

if [ -z "$LOG_DATA" ]; then
    echo "[WARNING] 분석할 데이터가 없습니다."
    exit 0
fi

# 로그 형식: [2026-05-26 20:51:01] PID:1570 CPU:0.0% MEM:4.2% DISK_USED:1%
# 필드: $1=[날짜  $2=시간]  $3=PID:N  $4=CPU:X%  $5=MEM:X%  $6=DISK_USED:X%
echo "$LOG_DATA" | awk '
NF >= 6 {
    ts = substr($1, 2) " " substr($2, 1, length($2)-1)

    split($4, ca, ":"); cpu = ca[2] + 0
    split($5, ma, ":"); mem = ma[2] + 0
    split($6, da, ":"); disk = da[2] + 0

    cpu_sum += cpu; mem_sum += mem; disk_sum += disk; count++

    if (count == 1 || cpu  > cpu_max)  { cpu_max  = cpu;  cpu_max_ts  = ts }
    if (count == 1 || cpu  < cpu_min)  { cpu_min  = cpu;  cpu_min_ts  = ts }
    if (count == 1 || mem  > mem_max)  { mem_max  = mem;  mem_max_ts  = ts }
    if (count == 1 || mem  < mem_min)  { mem_min  = mem;  mem_min_ts  = ts }
    if (count == 1 || disk > disk_max) { disk_max = disk; disk_max_ts = ts }
    if (count == 1 || disk < disk_min) { disk_min = disk; disk_min_ts = ts }
}
END {
    if (count == 0) { print "[WARNING] 데이터 없음"; exit }
    printf "\n    ====== STATISTICS REPORT ======\n"
    printf "      [CPU]\n"
    printf "        Average : %.1f%%\n",        cpu_sum  / count
    printf "        Maximum : %.1f%% at %s\n",  cpu_max,  cpu_max_ts
    printf "        Minimum : %.1f%% at %s\n",  cpu_min,  cpu_min_ts
    printf "      [Memory]\n"
    printf "        Average : %.1f%%\n",        mem_sum  / count
    printf "        Maximum : %.1f%% at %s\n",  mem_max,  mem_max_ts
    printf "        Minimum : %.1f%% at %s\n",  mem_min,  mem_min_ts
    printf "      [Disk]\n"
    printf "        Average : %.1f%%\n",        disk_sum / count
    printf "        Maximum : %.1f%% at %s\n",  disk_max, disk_max_ts
    printf "        Minimum : %.1f%% at %s\n",  disk_min, disk_min_ts
    printf "      [Samples]\n"
    printf "        Data Points: %d samples\n\n", count
}
'
