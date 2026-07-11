-- =====================================================
-- 예제 도메인: 도서 대여 (Book Rental)
-- 테이블 4개: category, book, member, rental
-- 1:N 관계 2개 이상:
--   category(1) -> book(N)
--   member(1)   -> rental(N)
--   book(1)     -> rental(N)
-- =====================================================

-- SQLite는 기본적으로 FK 제약을 강제하지 않으므로 매번 켜준다.
-- (DB 전용 문법: SQLite only)
PRAGMA foreign_keys = ON;

-- 기존 테이블이 있으면 삭제 후 재생성 (재실행 대비)
DROP TABLE IF EXISTS rental;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS category;

-- 1) 카테고리 (도서 분류)
CREATE TABLE category (
    id   INTEGER PRIMARY KEY AUTOINCREMENT, -- AUTOINCREMENT: SQLite 전용 문법
    name TEXT NOT NULL UNIQUE
);

-- 2) 회원
CREATE TABLE member (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    joined_at  DATE NOT NULL
);

-- 3) 도서 (category를 FK로 참조 -> 1:N)
CREATE TABLE book (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    title          TEXT NOT NULL,
    author         TEXT NOT NULL,
    category_id    INTEGER NOT NULL,
    published_year INTEGER,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 4) 대여 기록 (member, book을 FK로 참조 -> 1:N 두 개)
CREATE TABLE rental (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id    INTEGER NOT NULL,
    book_id      INTEGER NOT NULL,
    rental_date  DATE NOT NULL,
    return_date  DATE,               -- NULL이면 아직 반납 안 함
    status       TEXT NOT NULL DEFAULT '대여중', -- 대여중 / 반납완료 / 연체
    FOREIGN KEY (member_id) REFERENCES member(id),
    FOREIGN KEY (book_id)   REFERENCES book(id)
);

-- 인덱스: rental.book_id로 "이 책의 대여 이력"을 자주 조회하므로 조회 속도 향상 목적
CREATE INDEX idx_rental_book_id ON rental(book_id);
