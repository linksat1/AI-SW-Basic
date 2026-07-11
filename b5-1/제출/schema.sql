-- =====================================================
-- [내 주제]: 카페 주문 (Cafe Order)
-- 테이블 4개: customer, menu, orders, order_item
-- 1:N 관계 3개 (요구사항 2개 이상 충족):
--   customer(1) -> orders(N)
--   orders(1)   -> order_item(N)
--   menu(1)     -> order_item(N)
-- =====================================================

-- SQLite는 기본적으로 FK 제약을 강제하지 않으므로 매번 켜준다.
-- (DB 전용 문법: SQLite only)
PRAGMA foreign_keys = ON;

-- 기존 테이블이 있으면 삭제 후 재생성 (재실행 대비)
DROP TABLE IF EXISTS order_item;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS menu;
DROP TABLE IF EXISTS customer;

-- 1) 고객
CREATE TABLE customer (
    id        INTEGER PRIMARY KEY AUTOINCREMENT, -- AUTOINCREMENT: SQLite 전용 문법
    name      TEXT NOT NULL,
    phone     TEXT NOT NULL UNIQUE,
    joined_at DATE NOT NULL
);

-- 2) 메뉴
CREATE TABLE menu (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,          -- 커피 / 음료 / 디저트
    price    INTEGER NOT NULL
);

-- 3) 주문 (customer를 FK로 참조 -> 1:N)
CREATE TABLE orders (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date  DATE NOT NULL,
    status      TEXT NOT NULL DEFAULT '주문접수', -- 주문접수 / 제조중 / 완료 / 취소
    FOREIGN KEY (customer_id) REFERENCES customer(id)
);

-- 4) 주문 상세 (orders, menu를 FK로 참조 -> 1:N 두 개)
CREATE TABLE order_item (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    menu_id  INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (menu_id)  REFERENCES menu(id)
);

-- 인덱스: order_item.order_id로 "이 주문의 상세 내역"을 자주 조회하므로 조회 속도 향상 목적
CREATE INDEX idx_order_item_order_id ON order_item(order_id);
