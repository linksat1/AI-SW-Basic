-- =====================================================
-- 핵심 쿼리 15개 (위성 궤도/주파수)
-- 카테고리: 기본조회 4 / 조인 4(INNER 3 + LEFT 1) / 집계 3 / 서브쿼리 1 / 수정삭제 2 / 인덱스 1
-- 각 쿼리 위에 "무엇을 확인하는 쿼리인지" 한 줄 설명을 붙인다.
-- =====================================================

-- [기본조회 1] 최근 접수된 정지궤도(GSO) 위성망 신고 5건을 접수일 내림차순으로 확인한다.
SELECT ntc_id, adm, d_rcv
FROM notice
WHERE ntc_type = 'G'
ORDER BY d_rcv DESC
LIMIT 5;

-- [기본조회 2] 한국(KOR)이 신고한 위성망 목록을 확인한다.
SELECT ntc_id, adm, ntc_type, d_rcv
FROM notice
WHERE adm = 'KOR';

-- [기본조회 3] 동경 90도 이상에 위치한 정지궤도 위성의 궤도 위치를 경도 오름차순으로 확인한다.
SELECT sat_name, long_nom
FROM geo
WHERE long_nom >= 90
ORDER BY long_nom ASC;

-- [기본조회 4] Ku 대역(10,000~13,000MHz)에 속하는 주파수 대역을 확인한다.
SELECT ntc_id, emi_rcp, freq_min, freq_max
FROM freq
WHERE freq_min >= 10000 AND freq_max <= 13000
ORDER BY freq_min;

-- [조인-INNER 1] 위성망 이름과 신고국, 궤도 경도를 함께 확인한다.
SELECT n.ntc_id, n.adm, g.sat_name, g.long_nom
FROM notice n
INNER JOIN geo g ON n.ntc_id = g.ntc_id
ORDER BY g.long_nom;

-- [조인-INNER 2] 비정지궤도 신고의 신고국과 궤도면별 위성 수/경사각을 함께 확인한다.
SELECT n.ntc_id, n.adm, o.orb_id, o.nbr_sat_pl, o.inclin_ang
FROM notice n
INNER JOIN orbit o ON n.ntc_id = o.ntc_id
ORDER BY n.ntc_id, o.orb_id;

-- [조인-INNER 3] 한국(KOR)이 신고한 위성망의 주파수 대역을 위성 이름과 함께 확인한다.
SELECT n.adm, g.sat_name, f.emi_rcp, f.freq_min, f.freq_max
FROM notice n
INNER JOIN geo g ON n.ntc_id = g.ntc_id
INNER JOIN freq f ON n.ntc_id = f.ntc_id
WHERE n.adm = 'KOR';

-- [조인-LEFT 1] 모든 신고에 대해 정지궤도 위치 정보 유무를 확인한다. (비정지궤도 신고는 NULL로 남음)
SELECT n.ntc_id, n.adm, n.ntc_type, g.sat_name, g.long_nom
FROM notice n
LEFT JOIN geo g ON n.ntc_id = g.ntc_id
ORDER BY n.ntc_id;

-- [집계 1] 신고국(adm)별 위성망 신고 건수를 확인한다. (COUNT + GROUP BY)
SELECT adm, COUNT(*) AS 신고건수
FROM notice
GROUP BY adm
ORDER BY 신고건수 DESC;

-- [집계 2] 신고별 주파수 대역 개수와 평균 대역폭을 확인한다. (COUNT, AVG + GROUP BY)
SELECT ntc_id, COUNT(*) AS 대역수, ROUND(AVG(bdwdth), 1) AS 평균대역폭_kHz
FROM freq
GROUP BY ntc_id
ORDER BY 대역수 DESC;

-- [집계 3] 비정지궤도 신고별 전체 궤도면의 위성 수 합계를 확인한다. (SUM + GROUP BY)
SELECT ntc_id, SUM(nbr_sat_pl) AS 총위성수
FROM orbit
GROUP BY ntc_id;

-- [서브쿼리] 전체 평균 대역폭보다 넓은 주파수 대역을 확인한다.
SELECT ntc_id, emi_rcp, freq_min, freq_max, bdwdth
FROM freq
WHERE bdwdth > (SELECT AVG(bdwdth) FROM freq)
ORDER BY bdwdth DESC;

-- [수정 UPDATE] 아직 심사 중(st_cur=20)인 베트남(VTN) 신고를 처리 완료 상태(50)로 승인 처리한다.
UPDATE notice
SET st_cur = 50
WHERE adm = 'VTN' AND st_cur = 20;

-- [삭제 DELETE] 대역폭이 1,000,000kHz(=1GHz, Ka 대역 초광대역 피더링크)를 넘는 주파수 대역을 정리한다.
DELETE FROM freq
WHERE bdwdth >= 1000000;

-- [인덱스] freq.ntc_id로 notice와 JOIN하는 경우가 많아 idx_freq_ntc_id 인덱스를 적용했다.
-- (인덱스는 schema.sql에서 CREATE INDEX idx_freq_ntc_id ON freq(ntc_id); 로 생성됨)
-- 아래 쿼리로 인덱스가 실제로 사용되는지 실행 계획을 확인한다.
EXPLAIN QUERY PLAN
SELECT n.adm, f.freq_min, f.freq_max
FROM notice n
INNER JOIN freq f ON n.ntc_id = f.ntc_id
WHERE f.ntc_id = 125520109;
