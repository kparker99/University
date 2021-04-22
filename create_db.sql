DROP DATABASE IF EXISTS University;
CREATE DATABASE University; 
USE University;

CREATE TABLE role (
        role_id int (10) NOT NULL AUTO_INCREMENT,
		name varchar (50) NOT NULL,
        PRIMARY KEY (role_id)
        );
INSERT INTO role VALUES (1, 'Student');
INSERT INTO role VALUES (2, 'Teacher');
INSERT INTO role VALUES (3, 'Admin');

CREATE TABLE login (
        user_id varchar (50) NOT NULL,
		password varchar (50) NOT NULL,
        PRIMARY KEY (user_id)
        );
INSERT INTO login VALUES ('kparker', '1234');
INSERT INTO login VALUES ('swong', '3456');
INSERT INTO login VALUES ('dness', '4566');
INSERT INTO login VALUES ('swilliams', '8676');
INSERT INTO login VALUES ('hito', '1436');
INSERT INTO login VALUES ('freid', '8756');

CREATE TABLE course (
        course_id int (10) NOT NULL AUTO_INCREMENT,
		name varchar (50) NOT NULL,
		comments varchar (200),
        room int (2) NOT NULL,
        PRIMARY KEY (course_id)
        );
INSERT INTO course VALUES (1, 'Math', 'Intro to math', 3);
INSERT INTO course VALUES (2, 'Science', 'Intro to science', 3);

CREATE TABLE class (
        class_id int (10) NOT NULL AUTO_INCREMENT,
		course_id int (10) NOT NULL,
		year varchar (10) NOT NULL,
		semester char (2) NOT NULL,
        room varchar(8),
        instructor varchar(50) NOT NULL,
        FOREIGN KEY (course_id) REFERENCES course (course_id),
        PRIMARY KEY (class_id)
        );
INSERT INTO class VALUES (1, 1, '20-21', 's1', 'H34', 'Ness');
INSERT INTO class VALUES (2, 1, '20-21', 's2', 'G21', 'Ness');
INSERT INTO class VALUES (3, 2, '20-21', 's2', 'A12', 'Reid');

CREATE TABLE person (
        person_id int (10) NOT NULL AUTO_INCREMENT,
        role_id int (10) NOT NULL,
        user_id varchar (50) NOT NULL,
        f_name varchar (50) NOT NULL,
        l_name varchar (50) NOT NULL,
        address varchar (50) NOT NULL,
        city varchar (50) NOT NULL,
        state char (2) NOT NULL,
        phone varchar (20) DEFAULT NULL,
        dob date NOT NULL,
        email varchar (50) NOT NULL,
        photo_id varchar (50) DEFAULT NULL,
        PRIMARY KEY (person_id),
        FOREIGN KEY (role_id) REFERENCES role (role_id),
        FOREIGN KEY (user_id) REFERENCES login (user_id)
        );
INSERT INTO person VALUES (1, 1, 'kparker', 'Kevin', 'Parker', '123 Main St', 'Cumming', 'GA', '555-234-3546', '2000-03-14', 'k.parker@uni.edu', '\p\1s.jpg');
INSERT INTO person VALUES (2, 1, 'swong', 'Li', 'Wong', '1 Maple St', 'Alpharetta', 'GA', '555-324-3845', '1999-07-19', 'l.wong@uni.edu', '\p\2s.jpg');
INSERT INTO person VALUES (3, 2, 'dness', 'Douglas', 'Ness', '45 Powder Rd', 'Dallas', 'GA', '555-145-4535', '1983-10-21', 'doug.ness@uni.edu', '\p\3t.jpg');
INSERT INTO person VALUES (4, 1, 'swilliams', 'Shanice', 'Williams', '77 Alamont Rd', 'Cumming', 'GA', '555-139-3459', '2001-11-09', 's.williams@uni.edu', '\p\4s.jpg');
INSERT INTO person VALUES (5, 1, 'hito', 'Hiroshi', 'Ito', '94 Apple Way', 'Tacoma', 'WA', '555-865-3457', '2001-05-23', 'h.ito@uni.edu', '\p\5s.jpg');
INSERT INTO person VALUES (6, 2, 'freid', 'Francesco', 'Reid', '234 Sparrow Rd', 'Mobile', 'AL', '555-234-2756', '1970-02-02', 'francesco.reid@uni.edu', '\p\6t.jpg');

CREATE TABLE grades (
        class_id int (10) NOT NULL,
		test_id int (10) NOT NULL,
		person_id int (10) NOT NULL,
		test_date date NOT NULL,
		grade int (3) DEFAULT NULL,
        FOREIGN KEY (class_id) REFERENCES class (class_id),
        FOREIGN KEY (person_id) REFERENCES person (person_id)
        );
INSERT INTO grades VALUES (1, 1, 1, '2020-09-05', 85);
INSERT INTO grades VALUES (1, 1, 2, '2020-09-05', 91);
INSERT INTO grades VALUES (1, 1, 4, '2020-09-05', 87);
INSERT INTO grades VALUES (2, 1, 2, '2020-11-05', 65);
INSERT INTO grades VALUES (2, 1, 4, '2020-11-05', 90);
INSERT INTO grades VALUES (2, 1, 5, '2020-11-05', 94);
INSERT INTO grades VALUES (3, 1, 1, '2021-02-25', 87);
INSERT INTO grades VALUES (3, 1, 2, '2021-02-25', 76);
INSERT INTO grades VALUES (3, 1, 5, '2021-02-25', 78);
INSERT INTO grades VALUES (3, 2, 1, '2021-03-04', 87);
INSERT INTO grades VALUES (3, 2, 2, '2021-03-04', 99);
INSERT INTO grades VALUES (3, 2, 5, '2021-03-04', 85);

CREATE TABLE enrolled (
        enrolled_id int (10) NOT NULL AUTO_INCREMENT,
		person_id int (10) NOT NULL,
		class_id int (10) NOT NULL,
		role_id int (10) NOT NULL,
        FOREIGN KEY (class_id) REFERENCES class (class_id),
        FOREIGN KEY (role_id) REFERENCES role (role_id),
        FOREIGN KEY (person_id) REFERENCES person (person_id),
        PRIMARY KEY (enrolled_id)
        );
INSERT INTO enrolled VALUES (1, 1, 1, 1);
INSERT INTO enrolled VALUES (2, 2, 1, 1);
INSERT INTO enrolled VALUES (3, 3, 1, 2);
INSERT INTO enrolled VALUES (4, 4, 1, 1);
INSERT INTO enrolled VALUES (5, 2, 2, 1);
INSERT INTO enrolled VALUES (6, 3, 2, 2);
INSERT INTO enrolled VALUES (7, 4, 2, 1);
INSERT INTO enrolled VALUES (8, 5, 2, 1);
INSERT INTO enrolled VALUES (9, 1, 3, 1);
INSERT INTO enrolled VALUES (10, 2, 3, 1);
INSERT INTO enrolled VALUES (11, 5, 3, 1);
INSERT INTO enrolled VALUES (12, 6, 3, 2);