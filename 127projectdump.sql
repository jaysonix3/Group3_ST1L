DROP DATABASE IF EXISTS `cmsc127project`;
CREATE DATABASE IF NOT EXISTS `cmsc127project`;
USE `cmsc127project`;

CREATE TABLE IF NOT EXISTS `category` (
    `categoryid` int(3) NOT NULL DEFAULT 0,
    `categoryname` varchar(50) NOT NULL,
    `numberofactivetasks` int(3) NOT NULL DEFAULT '0',
    CONSTRAINT `category_categoryid_pk` PRIMARY KEY(`categoryid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `category` (`categoryid`, `categoryname`, `numberofactivetasks`) VALUES (0, 'no category', 0);
INSERT INTO `category` (`categoryid`, `categoryname`, `numberofactivetasks`) VALUES (1, 'CMSC 127', 0);

CREATE TABLE `task` (
    `taskid` int(3) NOT NULL AUTO_INCREMENT,
    `tasktitle` varchar(50) NOT NULL,
    `status` varchar(1) NOT NULL DEFAULT 'N',
    `duedate` date NOT NULL,
    `description` varchar(150),
    `categoryid` int(3) NOT NULL DEFAULT 0,
    CONSTRAINT `task_taskid_pk` PRIMARY KEY(`taskid`),
    CONSTRAINT `category_categoryid_fk` FOREIGN KEY (`categoryid`) REFERENCES category(`categoryid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `task` (`taskid`, `tasktitle`, `status`, `duedate`, `description`, `categoryid`) VALUES
    (1, 'Project Milestone 03', 'N', '2022-05-11', 'SQL Queries', 0);