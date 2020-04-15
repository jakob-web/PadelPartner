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
gender varchar (50),
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
);

create table profile (
    img varchar(1500),
    info varchar(2000),
    level integer,
    ort varchar (50),
    age integer,
    pid integer,
    PRIMARY KEY (pid),
    FOREIGN KEY (pid) REFERENCES person(pid)
);

create table registration (
    username varchar(50),
    password varchar(1000),
    pid integer,
    FOREIGN KEY (pid) REFERENCES person(pid),
    PRIMARY KEY (username)
);

create table Match (
    matchID integer,
    ort varchar(50),
    klass varchar(10), 
    antal integer,
    info varchar(1000),
    PRIMARY KEY (matchID)
);

CREATE SEQUENCE test_id_seq OWNED BY none;
ALTER TABLE person ALTER COLUMN pid SET DEFAULT nextval('test_id_seq');
UPDATE person
SET pid = nextval('test_id_seq');

CREATE SEQUENCE test_id_seq2 OWNED BY none;
ALTER TABLE profile ALTER COLUMN pid SET DEFAULT nextval('test_id_seq2');
UPDATE profile
SET pid = nextval('test_id_seq2'); 

CREATE SEQUENCE test_id_seq3 OWNED BY none;
ALTER TABLE registration ALTER COLUMN pid SET DEFAULT nextval('test_id_seq3');
UPDATE registration
SET pid = nextval('test_id_seq3');

CREATE SEQUENCE add_id OWNED BY none;
ALTER TABLE Match ALTER COLUMN MatchID SET DEFAULT nextval('add_id');
UPDATE Match
SET matchID = nextval('add_id');