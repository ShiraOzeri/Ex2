create database Ex2DB;
use Ex2DB;
create table MainTable(
full_nmea varchar(200) primary key ,
      latitude float(10),
      longitude float(10),
      height float(10),
      speed float(10),
      number_of_satellites int (5),
      time varchar(10)
);
describe MainTable;

#insert into MainTable values(12345,"noy","levi","Ariel",'1992/10/2',true);
