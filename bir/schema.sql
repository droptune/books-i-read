DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS publisher;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    cover TEXT,
    publisher INTEGER NOT NULL,
    category INTEGER NOT NULL,
    review TEXT,
    rating INTEGER,
    current_page INTEGER NOT NULL,
    total_pages INTEGER NOT NULL,
    year INTEGER,
    author TEXT,
    finished TEXT,
    FOREIGN KEY (author_id) REFERENCES user (id),
    FOREIGN KEY (publisher) REFERENCES publisher (id),
    FOREIGN KEY (category) REFERENCES category (id)
);

CREATE TABLE publisher (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    publisher_name TEXT UNIQUE NOT NULL
);

CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
);

INSERT INTO publisher (publisher_name)
VALUES
    ("O'Reilly"),
    ("Wiley"),
    ("Packt");

INSERT INTO category (category_name)
VALUES
    ('IT'),
    ('Business');
