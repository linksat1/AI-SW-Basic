-- =====================================================
-- 핵심 쿼리 15개
-- 카테고리: 기본조회 4 / 조인 4(INNER 3 + LEFT 1) / 집계 3 / 서브쿼리 1 / 수정삭제 2 / 인덱스 1
-- 각 쿼리 위에 "무엇을 확인하는 쿼리인지" 한 줄 설명을 붙인다.
-- =====================================================

-- [기본조회 1] 지금 대여 중인 기록을 최신 대여일 순으로 5건만 확인한다.
SELECT id, member_id, book_id, rental_date, status
FROM rental
WHERE status = '대여중'
ORDER BY rental_date DESC
LIMIT 5;

-- [기본조회 2] 'IT/컴퓨터' 카테고리(category_id = 5)에 속한 책만 확인한다.
SELECT id, title, author, published_year
FROM book
WHERE category_id = 5;

-- [기본조회 3] 2025년에 가입한 회원을 가입일 오름차순으로 확인한다.
SELECT name, email, joined_at
FROM member
WHERE joined_at >= '2025-01-01' AND joined_at < '2026-01-01'
ORDER BY joined_at ASC;

-- [기본조회 4] 가장 최근에 가입한 회원 3명을 확인한다.
SELECT name, joined_at
FROM member
ORDER BY joined_at DESC
LIMIT 3;

-- [조인-INNER 1] 지금 대여 중인 책과 빌린 회원 이름을 한 번에 확인한다.
SELECT m.name AS 회원, b.title AS 도서, r.rental_date, r.status
FROM rental r
INNER JOIN member m ON r.member_id = m.id
INNER JOIN book b ON r.book_id = b.id
WHERE r.status = '대여중';

-- [조인-INNER 2] 카테고리 이름과 함께 책 전체 목록을 확인한다.
SELECT c.name AS 카테고리, b.title, b.author
FROM book b
INNER JOIN category c ON b.category_id = c.id
ORDER BY c.name;

-- [조인-INNER 3] 연체 상태인 대여 건의 회원 이름/이메일과 책 제목을 확인한다.
SELECT m.name, m.email, b.title, r.rental_date
FROM rental r
INNER JOIN member m ON r.member_id = m.id
INNER JOIN book b ON r.book_id = b.id
WHERE r.status = '연체';

-- [조인-LEFT 1] 대여 기록이 0건인 회원도 빠짐없이 포함해 회원별 대여 횟수를 확인한다.
SELECT m.name, COUNT(r.id) AS 대여횟수
FROM member m
LEFT JOIN rental r ON m.id = r.member_id
GROUP BY m.id, m.name
ORDER BY 대여횟수 DESC;

-- [집계 1] 카테고리별로 보유한 책 권수를 확인한다. (COUNT + GROUP BY)
SELECT c.name AS 카테고리, COUNT(b.id) AS 보유권수
FROM category c
LEFT JOIN book b ON b.category_id = c.id
GROUP BY c.id, c.name
ORDER BY 보유권수 DESC;

-- [집계 2] 대여 상태(대여중/반납완료/연체)별 건수를 확인한다. (COUNT + GROUP BY)
SELECT status AS 상태, COUNT(*) AS 건수
FROM rental
GROUP BY status;

-- [집계 3] 카테고리별 평균 출간 연도를 확인한다. (AVG + GROUP BY)
SELECT c.name AS 카테고리, ROUND(AVG(b.published_year), 0) AS 평균출간연도
FROM book b
INNER JOIN category c ON b.category_id = c.id
GROUP BY c.id, c.name;

-- [서브쿼리] 대여 기록이 한 번도 없는 회원을 찾는다.
SELECT name, email
FROM member
WHERE id NOT IN (SELECT DISTINCT member_id FROM rental);

-- [수정 UPDATE] 반납일 없이 대여일이 오래된(2026-06-01 이전) 대여 건을 연체 처리한다.
UPDATE rental
SET status = '연체'
WHERE return_date IS NULL
  AND rental_date < '2026-06-01'
  AND status != '연체';

-- [삭제 DELETE] 오래된 반납완료 기록 중 테스트로 입력했던 1건을 삭제한다. (실제로는 신중하게 사용)
DELETE FROM rental
WHERE id = 15;

-- [인덱스] book_id로 대여 이력을 조회하는 경우가 많아 idx_rental_book_id 인덱스를 적용했다.
-- (인덱스는 01_schema.sql에서 CREATE INDEX idx_rental_book_id ON rental(book_id); 로 생성됨)
-- 아래 쿼리로 인덱스가 실제로 사용되는지 실행 계획을 확인한다.
EXPLAIN QUERY PLAN
SELECT * FROM rental WHERE book_id = 7;
