CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT,
	role INTEGER
);
	
CREATE TABLE additions (
	id SERIAL PRIMARY KEY,
	borough TEXT,
	genre TEXT,
	coordinates TEXT,
	creator_id INTEGER REFERENCES users,
	sent_at TIMESTAMP,
	visible INTEGER
);

CREATE TABLE reviews (
	id SERIAL PRIMARY KEY,
	addition_id INTEGER REFERENCES additions,
	stars INTEGER,
	comment TEXT,
	user_id INTEGER REFERENCES users,
	visible INTEGER,
	sent_at TIMESTAMP
);

CREATE TABLE sales (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	borough TEXT,
	comment TEXT,
	sent_at TIMESTAMP,
	visible INTEGER
);

CREATE TABLE purchases (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	borough TEXT,
	comment TEXT,
	sent_at TIMESTAMP,
	visible INTEGER
);
