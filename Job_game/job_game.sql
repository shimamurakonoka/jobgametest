create database job_game;
use job_game;

CREATE TABLE thread (
	thread_id int auto_increment primary key,
    thread_name varchar(50),
    user_id varchar(10)
);
CREATE TABLE board (
    comment_id  int auto_increment primary key,
    user_id varchar(10),
	comment VARCHAR(300),
    date varchar(50),
    thread_id int,
    thread_name varchar(50)
);
CREATE TABLE delete_board (
    delete_comment_id int auto_increment primary key,
    comment_id  int,
    date varchar(50),
    user_id varchar(10),
    comment VARCHAR(300),
	thread_name varchar(50),
	reason varchar (300),
    FOREIGN KEY(comment_id) REFERENCES board(comment_id)
);
-- create database job_game;
use job_game;

create table user
( id varchar(10) primary key,
  pw varchar(128),
  blessing1 int,
  blessing2 int,
  blessing3 int,
  herb int,
  score int,
  salt varchar(5)
);

create table admin
( id varchar(10) primary key,
  pw varchar(30)
);

insert into admin values
( "test", "test");

create table quiz(
id int auto_increment,
genre varchar(10),
quiz varchar(255),
degree_d int,
degree_i int,
answer int,
comment varchar(255),
PRIMARY KEY(id)
);

create table review
( id int auto_increment,
  user_id varchar(10),
  quiz_id varchar(50),
  FOREIGN KEY(user_id) REFERENCES user(user_id),
  FOREIGN KEY(quiz_id) REFERENCES quiz(quiz_id)
);

CREATE TABLE delete_thread (
    delete_thread_id int auto_increment primary key,
    thread_id int,
    thread_name varchar(50),
    user_id varchar(10),
    reason_2 varchar (300),
    FOREIGN KEY(thread_id) REFERENCES thread(thread_id)
);