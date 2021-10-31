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
INSERT INTO login VALUES ('lwong', '3456');
INSERT INTO login VALUES ('dness', '4566');
INSERT INTO login VALUES ('swilliams', '8676');
INSERT INTO login VALUES ('hito', '1436');
INSERT INTO login VALUES ('mbardem', '8756');
INSERT INTO login VALUES ('jsabathne', '2345');
INSERT INTO login VALUES ('nahmad', '3456');
INSERT INTO login VALUES ('mhamm', '5676');
INSERT INTO login VALUES ('jhenry', '5423');
INSERT INTO login VALUES ('jross', '5555');

CREATE TABLE course (
        course_number varchar (50) NOT NULL,
		course_name varchar (50) NOT NULL,
        hours int (2) NOT NULL,
		department varchar (200),
        course_description varchar (500),
        PRIMARY KEY (course_number)
        );
INSERT INTO course VALUES ('HSC315', 'Applied Psychology', 3, 'Human Services', 'In this course, students will learn key concepts in psychology and apply them to individual, community, and organizational settings. Students will explore the application of psychology in various disciplines. As a result, students will begin to develop skills that will further their career goals and further learning.');
INSERT INTO course VALUES ('BUS429', 'Leading Innovation', 3, 'Business Administration', 'This course focuses on creating a culture of innovation within an organization.');
INSERT INTO course VALUES ('ORL340', 'Leading Change in Organizations', 3, 'Organizational Leadership', "This course gives various opportunities for organizations to change, this course presents and discusses ideas to advance one's understanding of leading and managing strategic change for optimal financial, operational, and behavorial performance.");
INSERT INTO course VALUES ('HSC430', 'Statistical Theories and Applications', 3, 'Human Services', 'Analyzes parametric and nonparametric statistics commonly used in the human services.');
INSERT INTO course VALUES ('BUS374', 'Economics', 3, 'Business Administration', 'This course presents the principles and theories of micro and macroeconomics. It also explores its application to organizations, including decision making.');
INSERT INTO course VALUES ('BUS309', 'Interpersonal Effectiveness', 3, 'Business Administration', 'This course applies effective communication practices and principles to impact individuals, teams, and organizations.');
INSERT INTO course VALUES ('HSC496', 'Human Services Learning Outcomes Portfolio', 1, 'Human Services', "This course provides a capstone of students' major experience through assembling and organizing a portfolio of work demonstrating mastery of program learning outcomes within a Human Sciences major. Portfolios present evidence of students' understanding key theories, as well as application of these theories. Portfolios are also appropriate for students to share with current or prospective employers.");

CREATE TABLE class (
        class_id varchar (50) NOT NULL,
		course_number varchar (50) NOT NULL,
		start_date date NOT NULL,
		end_date date NOT NULL,
        room varchar(8),
        instructor varchar(50) NOT NULL,
        FOREIGN KEY (course_number) REFERENCES course (course_number),
        PRIMARY KEY (class_id)
        );
INSERT INTO class VALUES ('HSC315', 'HSC315', '2020-08-10', '2020-12-18', 'J38', 'hito');
INSERT INTO class VALUES ('BUS429', 'BUS429', '2020-08-10', '2020-12-18', 'D13', 'mbardem');
INSERT INTO class VALUES ('ORL340', 'ORL340', '2020-08-10', '2020-12-18', 'J28', 'mbardem');
INSERT INTO class VALUES ('HSC430', 'HSC430', '2020-08-10', '2020-12-18', 'J41', 'hito');
INSERT INTO class VALUES ('BUS374', 'BUS374', '2020-08-10', '2020-12-18', 'X70', 'jsabathne');
INSERT INTO class VALUES ('BUS309', 'BUS309', '2020-08-10', '2020-12-18', 'X74', 'jsabathne');
INSERT INTO class VALUES ('HSC496', 'HSC496', '2020-08-10', '2020-12-18', 'K1', 'mhamm');
INSERT INTO class VALUES ('HSC315_1', 'HSC315', '2022-01-11', '2022-05-28', 'J38', 'hito');
INSERT INTO class VALUES ('BUS429_1', 'BUS429', '2022-01-11', '2022-05-28', 'D13', 'mbardem');
INSERT INTO class VALUES ('ORL340_1', 'ORL340', '2022-01-11', '2022-05-28', 'J28', 'mbardem');
INSERT INTO class VALUES ('HSC430_1', 'HSC430', '2022-01-11', '2022-05-28', 'J41', 'hito');
INSERT INTO class VALUES ('BUS374_1', 'BUS374', '2022-01-11', '2022-05-28', 'X70', 'jsabathne');
INSERT INTO class VALUES ('BUS309_1', 'BUS309', '2022-01-11', '2022-05-28', 'X74', 'jsabathne');
INSERT INTO class VALUES ('HSC496_1', 'HSC496', '2022-01-11', '2022-05-28', 'K1', 'mhamm');
INSERT INTO class VALUES ('HSC315_2', 'HSC315', '2021-08-09', '2021-12-10', 'J38', 'hito');
INSERT INTO class VALUES ('BUS429_2', 'BUS429', '2021-08-09', '2021-12-10', 'D13', 'mbardem');
INSERT INTO class VALUES ('ORL340_2', 'ORL340', '2021-08-09', '2021-12-10', 'J28', 'mbardem');
INSERT INTO class VALUES ('HSC430_2', 'HSC430', '2021-08-09', '2021-12-10', 'J38', 'jhenry');
INSERT INTO class VALUES ('BUS374_2', 'BUS374', '2021-08-09', '2021-12-10', 'X77', 'jsabathne');
INSERT INTO class VALUES ('BUS309_2', 'BUS309', '2021-01-11', '2021-05-28', 'H13', 'nahmad');


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
        PRIMARY KEY (person_id),
        FOREIGN KEY (role_id) REFERENCES role (role_id),
        FOREIGN KEY (user_id) REFERENCES login (user_id)
        );
INSERT INTO person VALUES (1, 1, 'kparker', 'Kyle', 'Parker', '123 Main St', 'Mobile', 'AL', '555-234-3546', '2000-03-14', 'kparker@au.edu');
INSERT INTO person VALUES (2, 1, 'lwong', 'Li', 'Wong', '1 Maple St', 'Laurel', 'MS', '555-324-3845', '1999-07-19', 'lwong@au.edu');
INSERT INTO person VALUES (3, 1, 'dness', 'Douglas', 'Ness', '45 Powder Rd', 'Miami', 'FL', '555-145-4535', '1998-10-21', 'dness@au.edu');
INSERT INTO person VALUES (4, 1, 'swilliams', 'Shanice', 'Williams', '77 Alamont Rd', 'Aurora', 'IL', '555-139-3459', '2001-11-09', 'swilliams@au.edu');
INSERT INTO person VALUES (5, 2, 'hito', 'Hiroshi', 'Ito', '94 Apple Way', 'Cumming', 'GA', '555-865-3457', '1970-02-02', 'hito@au.edu');
INSERT INTO person VALUES (6, 2, 'mbardem', 'Monica', 'Bardem', '91 Oak St', 'Norcross', 'GA', '555-234-3467', '1983-04-29', 'mbardem@au.edu');
INSERT INTO person VALUES (7, 2, 'jsabathne', 'James', 'Sabathne', '34 Elm Way', 'Dallas', 'GA', '555-124-5672', '1981-02-18', 'jsabathne@au.edu');
INSERT INTO person VALUES (8, 2, 'nahmad', 'Nasir', 'Ahmad', '2659 Bowen Rd', 'Cumming', 'GA', '555-342-6879', '1968-08-30', 'nahmad@au.edu');
INSERT INTO person VALUES (9, 2, 'mhamm', 'Monique', 'Hamm', '284 Caspian Ln', 'Locust Grove', 'GA', '555-232-2765', '1977-06-06', 'mhamm@au.edu');
INSERT INTO person VALUES (10, 2, 'jhenry', 'Jacob', 'Henry', '483 Court Ct', 'Atlanta', 'GA', '555-789-2345', '1973-06-12', 'jhenry@au.edu');
INSERT INTO person VALUES (11, 3, 'jross', 'Jaylan', 'Ross', '345 Teal Ct', 'Atlanta', 'GA', '555-236-4653', '1980-12-13', 'jross@au.edu');


CREATE TABLE grades (
        class_id varchar (50) NOT NULL,
		user_id varchar (10) NOT NULL,
		test_number int (10) NOT NULL,
		test_date date NOT NULL,
		grade int (3) DEFAULT NULL,
        FOREIGN KEY (class_id) REFERENCES class (class_id),
        FOREIGN KEY (user_id) REFERENCES person (user_id)
        );
INSERT INTO grades VALUES ('HSC315', 'kparker',	1, '2021-01-14', 81);
INSERT INTO grades VALUES ('HSC315', 'kparker',	2, '2021-02-25', 92);
INSERT INTO grades VALUES ('HSC430', 'kparker',	1, '2021-01-15', 87);
INSERT INTO grades VALUES ('HSC430', 'kparker',	2, '2021-02-05', 89);
INSERT INTO grades VALUES ('HSC430', 'kparker',	3, '2021-02-26', 95);
INSERT INTO grades VALUES ('HSC496', 'kparker', 1, '2021-02-25', 97);
INSERT INTO grades VALUES ('BUS429', 'lwong', 1, '2021-01-14', 77);
INSERT INTO grades VALUES ('BUS429', 'lwong', 2, '2021-02-25', 72);
INSERT INTO grades VALUES ('BUS374', 'lwong', 1, '2021-02-25', 82);
INSERT INTO grades VALUES ('BUS309', 'lwong', 1, '2021-01-15', 83);
INSERT INTO grades VALUES ('BUS309', 'lwong', 2, '2021-02-05', 85);
INSERT INTO grades VALUES ('ORL340', 'lwong', 1, '2021-01-14', 72);
INSERT INTO grades VALUES ('ORL340', 'lwong', 2, '2021-02-25', 74);
INSERT INTO grades VALUES ('HSC315', 'dness', 1, '2021-01-14', 81);
INSERT INTO grades VALUES ('HSC315', 'dness', 2, '2021-02-25', 76);
INSERT INTO grades VALUES ('HSC430', 'dness', 1, '2021-01-15', 77);
INSERT INTO grades VALUES ('HSC430', 'dness', 2, '2021-02-05', 87);
INSERT INTO grades VALUES ('HSC430', 'dness', 3, '2021-02-26', 85);
INSERT INTO grades VALUES ('HSC496', 'dness', 1, '2021-02-25', 76);
INSERT INTO grades VALUES ('BUS429', 'swilliams', 1, '2021-01-14', 99);
INSERT INTO grades VALUES ('BUS429', 'swilliams', 2, '2021-02-25', 98);
INSERT INTO grades VALUES ('BUS374', 'swilliams', 1, '2021-02-25', 100);
INSERT INTO grades VALUES ('BUS309', 'swilliams', 1, '2021-01-15', 95);
INSERT INTO grades VALUES ('BUS309', 'swilliams', 2, '2021-02-05', 96);
INSERT INTO grades VALUES ('ORL340', 'swilliams', 1, '2021-01-14', 95);
INSERT INTO grades VALUES ('ORL340', 'swilliams', 2, '2021-02-25', 95);

CREATE TABLE enrolled (
        enrolled_id int (10) NOT NULL AUTO_INCREMENT,
		user_id varchar (50) NOT NULL,
		class_id varchar (50) NOT NULL,
		role_id int (10) NOT NULL,
        FOREIGN KEY (class_id) REFERENCES class (class_id),
        FOREIGN KEY (role_id) REFERENCES role (role_id),
        FOREIGN KEY (user_id) REFERENCES person (user_id),
        PRIMARY KEY (enrolled_id)
        );
INSERT INTO enrolled VALUES (1,	'kparker', 'HSC315', 1);
INSERT INTO enrolled VALUES (2,	'kparker', 'HSC430', 1);
INSERT INTO enrolled VALUES (3,	'kparker', 'HSC496', 1);
INSERT INTO enrolled VALUES (4,	'lwong', 'BUS429', 1);
INSERT INTO enrolled VALUES (5,	'lwong', 'BUS374', 1);
INSERT INTO enrolled VALUES (6,	'lwong', 'BUS309', 1);
INSERT INTO enrolled VALUES (7,	'lwong', 'ORL340', 1);
INSERT INTO enrolled VALUES (8,	'dness', 'HSC315', 1);
INSERT INTO enrolled VALUES (9,	'dness', 'HSC430', 1);
INSERT INTO enrolled VALUES (10, 'dness', 'HSC496',	1);
INSERT INTO enrolled VALUES (11, 'swilliams', 'BUS429',	1);
INSERT INTO enrolled VALUES (12, 'swilliams', 'BUS374',	1);
INSERT INTO enrolled VALUES (13, 'swilliams', 'BUS309',	1);
INSERT INTO enrolled VALUES (14, 'swilliams', 'ORL340',	1);
INSERT INTO enrolled VALUES (15, 'hito',	'HSC315', 2);
INSERT INTO enrolled VALUES (16, 'mbardem', 'BUS429', 2);
INSERT INTO enrolled VALUES (17, 'mbardem', 'ORL340', 2);
INSERT INTO enrolled VALUES (18, 'hito',	'HSC430', 2);
INSERT INTO enrolled VALUES (19, 'jsabathne', 'BUS374', 2);
INSERT INTO enrolled VALUES (20, 'nahmad', 'BUS309', 2);
INSERT INTO enrolled VALUES (21, 'mhamm', 'HSC496', 2);
