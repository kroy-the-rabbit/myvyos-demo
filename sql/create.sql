create table if not exists myvyos.users (id integer unsigned not null primary key auto_increment, username varchar(48) not null, password varchar(128) not null, signup_date datetime);
