#!/bin/bash
# =============================================================
# log_archive.sh - 시간 기반 로그 보존 정책
# - 7일 경과 로그 압축 → /var/log/monitor/agent-app/archive/ 이동
# - 30일 경과 아카이브 삭제
# =============================================================

LOG_DIR="/var/log/agent-app"
ARCHIVE_DIR="/var/log/monitor/agent-app/archive"

# ---- 아카이브 디렉토리 생성 ----
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir -p "$ARCHIVE_DIR" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "[ERROR] 아카이브 디렉토리 생성 실패: $ARCHIVE_DIR (권한 부족)"
        exit 1
    fi
    echo "[INFO] 아카이브 디렉토리 생성: $ARCHIVE_DIR"
fi

# ---- 로그 디렉토리 존재 확인 ----
if [ ! -d "$LOG_DIR" ]; then
    echo "[ERROR] 로그 디렉토리 없음: $LOG_DIR"
    exit 1
fi

# ---- 7일 경과 로그 압축 → 아카이브 이동 ----
echo "[INFO] 7일 경과 로그 파일 압축 중..."
OLD_FILES=$(find "$LOG_DIR" -name "*.log" -mtime +7 2>/dev/null)

if [ -z "$OLD_FILES" ]; then
    echo "[INFO] 압축 대상 없음 (7일 이내 로그만 존재)"
else
    echo "$OLD_FILES" | while IFS= read -r file; do
        BASENAME=$(basename "$file")
        DEST="${ARCHIVE_DIR}/${BASENAME}.$(date +%Y%m%d).gz"
        if gzip -c "$file" > "$DEST" 2>/dev/null; then
            rm -f "$file"
            echo "[OK] 압축/이동: $file → $DEST"
        else
            echo "[WARNING] 압축 실패: $file"
        fi
    done
fi

# ---- 30일 경과 아카이브 삭제 ----
echo "[INFO] 30일 경과 아카이브 파일 삭제 중..."
OLD_ARCHIVES=$(find "$ARCHIVE_DIR" -name "*.gz" -mtime +30 2>/dev/null)

if [ -z "$OLD_ARCHIVES" ]; then
    echo "[INFO] 삭제 대상 없음 (30일 이내 아카이브만 존재)"
else
    echo "$OLD_ARCHIVES" | while IFS= read -r archive; do
        rm -f "$archive"
        echo "[OK] 삭제: $archive"
    done
fi

echo "[INFO] 로그 보존 정책 완료"
