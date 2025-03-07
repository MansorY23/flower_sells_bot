create schema if not exists public;

drop table if exists public.order;
CREATE TABLE if not exists public.order (
	id bigserial primary key,
	amount integer not null ,
	order_sum integer not null,
	product_id integer,
	flower_point_id integer not null,
	created_at timestamp not NULL default now(),
	updated_at timestamp
);

drop table if exists public.flower_point;
create table if not exists public.flower_point
(
	id bigserial primary key,
	address text NOT NULL, 
	created_at timestamp NOT NULL default now(),
	updated_at timestamp

);


drop table if exists public.product;
create table if not exists public.product
(
	id bigserial primary key,
	product_name text NOT NULL,
	price integer NOT NULL,
	created_at timestamp NOT NULL default now(),
	updated_at timestamp
);

drop table if exists public.stock;
create table if not exists public.stock
(
	id bigserial primary key,
	product_id integer,
	flower_point_id integer,
    quantity integer NOT NULL DEFAULT 0,
	created_at timestamp NOT NULL default now(),
	updated_at timestamp
);

drop table if exists public.user;
CREATE TABLE IF NOT EXISTS public.user
(
	id bigserial primary key,
	name text NOT NULL,
	telegram_id bigint NOT NULL,
	flower_point_id integer
	created_at timestamp NOT NULL default now(),
	updated_at timestamp,
)
;

alter table public.order drop constraint IF EXISTS fk_flower_point;
alter table public.order 
	add constraint fk_flower_point
	foreign key (flower_point_id)
	references public.flower_point (id)
	on delete NO ACTION
;
alter table public.order drop constraint IF EXISTS fk_product;
alter table public.order 
	add constraint fk_product
	foreign key (product_id)
	references public.product (id) 
	on delete NO ACTION

;
alter table public.stock drop constraint IF EXISTS fk_product;
alter table public.stock 
	add constraint fk_product
	foreign key (product_id)
	references public.product (id)
	ON DELETE CASCADE
;

alter table public.stock drop constraint IF EXISTS fk_flower_point;
alter table public.stock 
	add constraint fk_flower_point
	foreign key (flower_point_id)
	references public.flower_point (id)
	ON DELETE CASCADE
;
alter table public.user drop constraint IF EXISTS fk_flower_point;
alter table public.user 
	add constraint fk_flower_point
	foreign key (flower_point_id)
	references public.flower_point (id)
	ON DELETE NO ACTION
;
	
insert into public.flower_point (address) values
		('Алтын'),
		('Южка'),
		('Магнит'),
		('Сбербанк')
;

insert into public.product (product_name, price) values 
		('Белые тюльпаны', 130),
		('Жёлтые тюльпаны', 130),
		('Красные тюльпаны', 130),
		('Розовые тюльпаны', 130),
		('Огненные тюльпаны', 130)
;

INSERT INTO public.product_flower_point (product_id, flower_point_id, quantity) values 
	(1, 1, 500),
	(1, 2, 500),
	(1, 3, 500),
	(1, 4, 500)
;

INSERT INTO public.user (name, telegram_id, flower_point_id) values
	 ('Алина', 1272101647, 3),
	 ('Аня', 1025023173, 4),
	 ('Элвин', 1076704470, 2)
	 ('Сергей', 890462786, 1)
	;
	

--CREATE TABLE IF NOT EXISTS public.order_product
--(
--	order_id integer,
--	product_id integer
--	CONSTRAINT order_product_pkey PRIMARY KEY(order_id, product_id)
--);
