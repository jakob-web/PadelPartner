drop database if exits padelpartner;

drop table if exits person;

create table person (
pnr integer, 
namn char(30), 
level integer,
info char(100),
PRIMARY KEY (pnr)
);

create table person (
pnr BIGINT CONSTRAINT TenDigits CHECK (pnr BETWEEN 1000000000 and 9999999999),
namn varchar(100),
level int,
info varchar(1000),
PRIMARY KEY (pnr)
);


create table ort (
ortID integer,
stad char(40),
PRIMARY KEY (ortID)
);

create table profile (
id integer,
username char(50),
password char(50),
PRIMARY KEY (id)
); 
