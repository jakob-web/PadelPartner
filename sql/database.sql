drop database if exits padelpartner;

drop table if exits person;

create table person (
pnr integer, 
namn char(30), 
level integer,
info char(100)
PRIMARY KEY pnr
);

create table ort (
ortID integer,
stad char(40)
PRIMARY KEY ortID
);
