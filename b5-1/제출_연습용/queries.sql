-- =====================================================
-- 핵심 쿼리 15개
-- 카테고리: 기본조회 4 / 조인 4(INNER 3 + LEFT 1) / 집계 3 / 서브쿼리 1 / 수정삭제 2 / 인덱스 1
-- 각 쿼리 위에 "무엇을 확인하는 쿼리인지" 한 줄 설명을 붙인다.
-- =====================================================

-- [기본조회 1] 완료된 주문을 최신 주문일 순으로 5건만 확인한다.
SELECT id, customer_id, order_date, status
FROM orders
WHERE status = '완료'
ORDER BY order_date DESC
LIMIT 5;

-- [기본조회 2] '커피' 카테고리 메뉴만 확인한다.
SELECT id, name, price
FROM menu
WHERE category = '커피';

-- [기본조회 3] 2025년 3월 이후 가입한 고객을 가입일 오름차순으로 확인한다.
SELECT name, phone, joined_at
FROM customer
WHERE joined_at >= '2025-03-01'
ORDER BY joined_at ASC;

-- [기본조회 4] 가격이 가장 비싼 메뉴 3개를 확인한다.
SELECT name, price
FROM menu
ORDER BY price DESC
LIMIT 3;

-- [조인-INNER 1] 주문마다 어떤 고객이 주문했는지 이름과 함께 확인한다.
SELECT o.id AS 주문번호, c.name AS 고객, o.order_date, o.status
FROM orders o
INNER JOIN customer c ON o.customer_id = c.id
ORDER BY o.order_date;

-- [조인-INNER 2] 주문 상세(메뉴 이름, 수량)를 주문번호와 함께 확인한다.
SELECT oi.order_id AS 주문번호, m.name AS 메뉴, oi.quantity AS 수량
FROM order_item oi
INNER JOIN menu m ON oi.menu_id = m.id
ORDER BY oi.order_id;

-- [조인-INNER 3] 취소된 주문을 한 고객의 이름과 연락처를 확인한다.
SELECT c.name, c.phone, o.order_date
FROM orders o
INNER JOIN customer c ON o.customer_id = c.id
WHERE o.status = '취소';

-- [조인-LEFT 1] 주문 기록이 0건인 고객도 빠짐없이 포함해 고객별 주문 횟수를 확인한다.
SELECT c.name, COUNT(o.id) AS 주문횟수
FROM customer c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY 주문횟수 DESC;

-- [집계 1] 메뉴별 총 판매 수량을 확인한다. (SUM + GROUP BY)
SELECT m.name AS 메뉴, SUM(oi.quantity) AS 총판매수량
FROM order_item oi
INNER JOIN menu m ON oi.menu_id = m.id
GROUP BY m.id, m.name
ORDER BY 총판매수량 DESC;

-- [집계 2] 주문 상태별 건수를 확인한다. (COUNT + GROUP BY)
SELECT status AS 상태, COUNT(*) AS 건수
FROM orders
GROUP BY status;

-- [집계 3] 카테고리별 평균 메뉴 가격을 확인한다. (AVG + GROUP BY)
SELECT category AS 카테고리, ROUND(AVG(price), 0) AS 평균가격
FROM menu
GROUP BY category;

-- [서브쿼리] 주문 이력이 한 번도 없는 고객을 찾는다.
SELECT name, phone
FROM customer
WHERE id NOT IN (SELECT DISTINCT customer_id FROM orders);

-- [수정 UPDATE] '주문접수' 상태의 주문을 '제조중'으로 진행 처리한다.
UPDATE orders
SET status = '제조중'
WHERE status = '주문접수';

-- [삭제 DELETE] 취소된 주문의 상세 내역을 먼저 지운 뒤, 취소된 주문 1건을 삭제한다. (FK 제약 때문에 자식부터 삭제)
DELETE FROM order_item
WHERE order_id = (SELECT id FROM orders WHERE status = '취소' LIMIT 1);

DELETE FROM orders
WHERE status = '취소';

-- [인덱스] order_id로 주문 상세를 조회하는 경우가 많아 idx_order_item_order_id 인덱스를 적용했다.
-- (인덱스는 schema.sql에서 CREATE INDEX idx_order_item_order_id ON order_item(order_id); 로 생성됨)
-- 아래 쿼리로 인덱스가 실제로 사용되는지 실행 계획을 확인한다.
EXPLAIN QUERY PLAN
SELECT * FROM order_item WHERE order_id = 1;
