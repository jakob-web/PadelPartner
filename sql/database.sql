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
    level varchar(2),
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
    skapare varchar(100),
    booked int,
    datum varchar(20),
    kön varchar(10),
    FOREIGN KEY (skapare) REFERENCES registration(username),
    PRIMARY KEY (matchID)
);

create table booking (
    matchid integer,
    username varchar(50),
    creatorName varchar(50),
    booked int,
);

create table msg (
    writer varchar(50),
    reciever varchar(50),
    message varchar(3000),
    date timestamp DEFAULT CURRENT_TIMESTAMP
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