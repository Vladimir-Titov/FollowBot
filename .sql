CREATE TABLE shop(
	shop_id SERIAL PRIMARY KEY,
	name varchar(50) NOT NULL,
	is_archive boolean default False);

create table users(
	user_id integer primary key,
	name text,
	username text,
	create_date timestamp default now(),
	is_archive boolean default False,
	UNIQUE(user_id));

create table product(
	product_id serial primary key,
	name text not null,
	link text not null,
	price numeric(8,2) not null,
	last_price numeric (8,2),
	user_id integer,
	shop_id integer,
	last_update_date timestamp ,
	is_archive boolean default false,
	FOREIGN KEY (shop_id) REFERENCES shop (shop_id) on delete set null,
	FOREIGN KEY (user_id) REFERENCES users (user_id) on delete set null);