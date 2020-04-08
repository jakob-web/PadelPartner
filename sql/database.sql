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

-- # NEW: 
create table person (
    pid integer,
    name varchar(100),
    email varchar(100),
    gender varchar(50),
    PRIMARY KEY (pid)
)

create table profile (
    img varchar(1500),
    info varchar(2000),
    level integer,
    age integer,
    pid integer,
    PRIMARY KEY (pid),
    FOREIGN KEY (pid) REFERENCES person (pid)
)

create table registration (
    username varchar(50),
    password varchar(50),
    PRIMARY KEY (username)
)