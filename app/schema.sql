DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS patients;

CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userrole TEXT DEFAULT "GUEST",
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE patients(
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    admission_date DATETIME NOT NULL,
    report_url TEXT NOT NULL
);
