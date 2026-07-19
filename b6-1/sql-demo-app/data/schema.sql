-- =====================================================
-- 연습 주제: 위성 궤도/주파수 (Satellite Orbit & Frequency)
-- 실제 위성망 등록 DB_3075에서
-- 발췌한 데이터를 SQLite용으로 옮겼습니다.
-- 테이블 4개: notice, geo, orbit, freq
-- 1:N 관계 3개 (요구사항 2개 이상 충족):
--   notice(1) -> geo(N)    정지궤도(GSO) 위성의 궤도 위치
--   notice(1) -> orbit(N)  비정지궤도(NGSO) 위성의 궤도면 정보
--   notice(1) -> freq(N)   신고에 포함된 주파수 대역
-- =====================================================

-- SQLite는 기본적으로 FK 제약을 강제하지 않으므로 매번 켜준다.
-- (DB 전용 문법: SQLite only)
PRAGMA foreign_keys = ON;

-- 기존 테이블이 있으면 삭제 후 재생성 (재실행 대비)
DROP TABLE IF EXISTS freq;
DROP TABLE IF EXISTS orbit;
DROP TABLE IF EXISTS geo;
DROP TABLE IF EXISTS notice;

-- 1) 신고(Notice) — ITU 등록 원장 (부모 테이블)
CREATE TABLE notice (
    ntc_id   INTEGER PRIMARY KEY,   -- ITU 신고번호(Notice ID). 실제 원본 PK 값을 그대로 사용
    adm      TEXT NOT NULL,         -- 신고 행정기관(국가) 코드, 예: KOR, CHN, RUS
    ntc_type TEXT NOT NULL,         -- 'G' = 정지궤도(GSO), 'N' = 비정지궤도(NGSO)
    d_rcv    DATE NOT NULL,         -- ITU 접수일
    ntf_rsn  TEXT,                  -- 신고 사유 코드 (N=신규, C=변경 등)
    st_cur   INTEGER                -- 현재 처리 상태 코드
);

-- 2) 정지궤도 위치 정보 (notice를 FK로 참조 -> 1:N, GSO 신고에만 존재)
CREATE TABLE geo (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    ntc_id   INTEGER NOT NULL,
    sat_name TEXT NOT NULL UNIQUE,  -- 위성망 이름, 예: KOREASAT-116K-2
    long_nom REAL NOT NULL,         -- 공칭 궤도 경도(°), 음수=서경, 양수=동경
    tol_east REAL,                  -- 동쪽 허용 오차(°)
    tol_west REAL,                  -- 서쪽 허용 오차(°)
    FOREIGN KEY (ntc_id) REFERENCES notice(ntc_id)
);

-- 3) 비정지궤도 궤도면 정보 (notice를 FK로 참조 -> 1:N, NGSO 신고에만 존재)
CREATE TABLE orbit (
    ntc_id     INTEGER NOT NULL,
    orb_id     INTEGER NOT NULL,    -- 신고 내 궤도면 번호 (같은 ntc_id 안에서 1부터 증가)
    nbr_sat_pl INTEGER NOT NULL,    -- 해당 궤도면의 위성 수
    inclin_ang REAL,                -- 궤도 경사각(°)
    apog_km    REAL,                -- 원지점 고도(km)
    perig_km   REAL,                -- 근지점 고도(km)
    op_ht_km   REAL,                -- 운용 고도(km)
    PRIMARY KEY (ntc_id, orb_id),   -- 복합 PK: 같은 신고 안에서 궤도면 번호로 구분
    FOREIGN KEY (ntc_id) REFERENCES notice(ntc_id)
);

-- 4) 주파수 대역 (notice를 FK로 참조 -> 1:N)
CREATE TABLE freq (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    ntc_id   INTEGER NOT NULL,
    emi_rcp  TEXT NOT NULL,         -- 'E' = 우주국 송신(하향 링크), 'R' = 우주국 수신(상향 링크)
    freq_min REAL NOT NULL,         -- 대역 하한 (MHz)
    freq_max REAL NOT NULL,         -- 대역 상한 (MHz)
    bdwdth   REAL,                  -- 대역폭 (kHz)
    FOREIGN KEY (ntc_id) REFERENCES notice(ntc_id)
);

-- 인덱스: freq는 4개 테이블 중 행이 가장 많고 ntc_id로 JOIN이 잦으므로 조회 속도 향상 목적
CREATE INDEX idx_freq_ntc_id ON freq(ntc_id);
CREATE INDEX idx_orbit_ntc_id ON orbit(ntc_id);
