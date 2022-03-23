# -*- coding: utf-8 -*- 
#!/usr/bin/env python
import sqlite3 as dbi
import os

### 01. TABLE: RAW_LIST
SQL_CREATE_TABLE_RAW_LIST = """
create table if not exists raw_list (
	pageno int primary key,
	html text
);
"""

SQL_INSERT_INTO_RAW_LIST = """
insert or ignore into raw_list values(?,?)
"""

SQL_QUERY_RAW_LIST = """
select html from raw_list order by pageno;
"""

SQL_QUERY_LAST_PAGENO = """
select max(pageno) from raw_list order by pageno;
"""


### 02. TABLE: RAW_LIST
SQL_CREATE_TABLE_GAME_LIST = """
create table if not exists game_list (
	id int primary key,
	name varchar(256),
	price int,
	release_date varchar(16)
);
"""

SQL_INSERT_INTO_GAME_LIST = """
insert or ignore into game_list values(?,?,?,?)
"""




# create database and table
def create_database(dsn, truncate=False):
	if truncate:
		if os.path.exists(dsn):
			os.remove(dsn)
	db = dbi.connect(dsn)
	db.execute(SQL_CREATE_TABLE_RAW_LIST)
	db.execute(SQL_CREATE_TABLE_GAME_LIST)
	return db

# insert record into table
def insert_record(db, sql, values):
	db.execute(sql, values)
	db.commit()

# get last pageno
def get_last_pageno(db):
	cursor = db.cursor()
	rows = cursor.execute(SQL_QUERY_LAST_PAGENO)
	for row in rows:
		if row[0] == None:
			return 0
		return row[0]
	return 0;
