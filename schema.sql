DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  surname TEXT UNIQUE NOT NULL,
  data_dodania datetime NOT NULL
);

INSERT into users VALUES(0, "Jan", "Testowy", "2021-06-21")
