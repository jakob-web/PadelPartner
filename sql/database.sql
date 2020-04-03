drop database if exits padelpartner;

drop table if exits person;


create table person (
pnr BIGINT CONSTRAINT TenDigits CHECK (pnr BETWEEN 1000000000 and 9999999999),
namn varchar(100),
level int,
info varchar(1000),
PRIMARY KEY (pnr)
);


create table ort (
ortID integer,
stad varchar(40),
PRIMARY KEY (ortID)
);

create table profile (
id integer,
username varchar(50),
password varchar(50),
PRIMARY KEY (id)
); 

create table profile1 (
id integer
gender varchar (50)
info varchar (1500)
PRIMARY KEY (id)
)
