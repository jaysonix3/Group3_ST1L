# CMSC 127 PROJECT 

## Group 3 - ST1L Members: 
	- Jamie Mari O. Ciron
	- Ralph Jason D. Corrales
	- Ariel Raphael F. Magno
	- Marie Sophia Therese T. Nakashima

## Requirement(s):
	- PIP for Python 
	- pip install mysql-connector-python
  	- MariaDB = database to be used

## User and database in MariadDB:
	username: test
	password: cmsc127
	database name: cmsc127project
- Note: if using root, update app.py

## Creation of user in MariaDB: 
	- login as root user
	- run the following commands: 
		- CREATE USER 'test'@localhost IDENTIFIED BY 'cmsc127';
		- GRANT ALL PRIVILEGES ON cmsc127project.* TO 'test'@'localhost';
	- login as test
	- run the command: 
		- source 127projectdump.sql;

## Running the program: 
	- python app.py
