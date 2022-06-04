DROP DATABASE IF EXISTS `cmsc127project`;
CREATE DATABASE IF NOT EXISTS `cmsc127project`;
USE `cmsc127project`;
CREATE TABLE IF NOT EXISTS `category` (
    `categoryid` int(3) AUTO_INCREMENT,
    `categoryname` varchar(50) NOT NULL,
    `numberofactivetasks` int(3) NOT NULL DEFAULT '0',
    CONSTRAINT `category_categoryid_pk` PRIMARY KEY(`categoryid`), 
    CONSTRAINT `category_categoryname_uk` UNIQUE(`categoryname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `task` (
    `taskid` int(3) AUTO_INCREMENT,
    `tasktitle` varchar(50) NOT NULL,
    `status` varchar(1) NOT NULL DEFAULT 'N',
    `duedate` date NOT NULL,
    `description` varchar(150),
    `categoryid` int(3) NOT NULL DEFAULT 1,
    CONSTRAINT `task_taskid_pk` PRIMARY KEY(`taskid`),
    CONSTRAINT `category_categoryid_fk` FOREIGN KEY (`categoryid`) REFERENCES category(`categoryid`),
    CONSTRAINT `task_tasktitle_uk` UNIQUE(`tasktitle`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `category` (`categoryname`, `numberofactivetasks`) VALUES ('no category', 0);
INSERT INTO `category` (`categoryname`, `numberofactivetasks`) VALUES ('CMSC 127', 0);
INSERT INTO `category` (`categoryname`, `numberofactivetasks`) VALUES ('CMSC 100', 0);
INSERT INTO `category` (`categoryname`, `numberofactivetasks`) VALUES ('CMSC 131', 0);
INSERT INTO `category` (`categoryname`, `numberofactivetasks`) VALUES ('CMSC 141', 0);
INSERT INTO `category` (`categoryname`, `numberofactivetasks`) VALUES ('academic', 0);
INSERT INTO `category` (`categoryname`, `numberofactivetasks`) VALUES ('org-related', 0);
INSERT INTO `category` (`categoryname`, `numberofactivetasks`) VALUES ('lovelife', 0);
INSERT INTO `category` (`categoryname`, `numberofactivetasks`) VALUES ('money', 0);
INSERT INTO `category` (`categoryname`, `numberofactivetasks`) VALUES ('to_watch', 0);

INSERT INTO `task` (`tasktitle`, `status`, `duedate`, `description`) VALUES
    ('Project Milestone 03', 'N', '2022-05-11', 'SQL Queries 1');
INSERT INTO `task` (`tasktitle`, `status`, `duedate`, `description`) VALUES
    ('Project Milestone 04', 'Y', '2022-05-31', 'SQL Queries 2');
INSERT INTO `task` (`tasktitle`, `status`, `duedate`, `description`) VALUES
    ('task 1', 'N', '2021-09-11', 'description 1');
INSERT INTO `task` (`tasktitle`, `status`, `duedate`, `description`) VALUES
    ('task 2', 'N', '2010-07-21', 'description 2');
INSERT INTO `task` (`tasktitle`, `status`, `duedate`, `description`) VALUES
    ('task 3', 'Y', '2020-08-13', 'description 3');
INSERT INTO `task` (`tasktitle`, `status`, `duedate`, `description`) VALUES
    ('task 4', 'N', '2021-10-24', 'description 4');
INSERT INTO `task` (`tasktitle`, `status`, `duedate`, `description`) VALUES
    ('task 5', 'N', '2021-11-30', 'description 5');
INSERT INTO `task` (`tasktitle`, `status`, `duedate`, `description`) VALUES
    ('task 6', 'N', '2020-01-28', 'description 6');
INSERT INTO `task` (`tasktitle`, `status`, `duedate`, `description`) VALUES
    ('task 7', 'N', '2019-05-19', 'description 7');
INSERT INTO `task` (`tasktitle`, `status`, `duedate`, `description`) VALUES
    ('task 8', 'N', '2011-03-18', 'description 8');
INSERT INTO `task` (`tasktitle`, `status`, `duedate`, `description`) VALUES
    ('task 9', 'N', '2018-02-25', 'description 9');
INSERT INTO `task` (`tasktitle`, `status`, `duedate`, `description`) VALUES
    ('task 10', 'N', '2020-06-07', 'description 10');
