# CMSC 127 PROJECT 

## Group 3 Members: 
	- Jamie Mari O. Ciron
	- Ralph Jason D. Corrales
	- Ariel Raphael F. Magno
	- Marie Sophia Therese T. Nakashima

## Requirement(s):
	- PIP for Python (reference: https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/)
	- pip install mysql-connector-python
  - app.py = python 3.x with PIP installed
  - MariaDB = database to be used

## User in MariadDB:
	username: test
	password: cmsc127

	- Note: if using root, update app.py

## Creation of user in MariaDB: 
	- login as root user
	- run the following commands: 
		- CREATE USER 'test'@localhost IDENTIFIED BY 'cmsc127';
		- GRANT ALL PRIVILEGES ON cmsc127project.* TO 'test'@'localhost';

## Notes:
	- use 'source 127projectdump.sql;'

## Running the program: 
	- python app.py
