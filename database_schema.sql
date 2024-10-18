PRAGMA foreign_keys=off;


DROP TABLE IF EXISTS user_credentials;
DROP TABLE IF EXISTS user_information;
DROP TABLE IF EXISTS systems_administrator;
DROP TABLE IF EXISTS grad_secretary;
DROP TABLE IF EXISTS faculty_advisor;
DROP TABLE IF EXISTS graduate_student;
DROP TABLE IF EXISTS alumni;

DROP TABLE IF EXISTS program;
DROP TABLE IF EXISTS curriculum;

DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS prerequisite;
DROP TABLE IF EXISTS course_taken;
DROP TABLE IF EXISTS forms;
DROP TABLE IF EXISTS forms_classes;
DROP TABLE IF EXISTS course_taken;

DROP TABLE IF EXISTS thesis;
DROP TABLE IF EXISTS graduation_application;

CREATE TABLE IF NOT EXISTS user_credentials (
    user                VARCHAR(20) UNIQUE NOT NULL,
    pass                VARCHAR(20) NOT NULL,
    user_id             INTEGER UNIQUE NOT NULL
);
--START OF user_credentials TABLE--

--DEFAULT TEST ACCOUNTS--
INSERT INTO user_credentials VALUES 
('adminuser', 'adminpass', 0),
('secretaryuser', 'secretarypass', 1),
('advisoruser', 'advisorpass', 2),
('studentuser', 'studentpass', 3),
('alumniuser', 'alumnipass', 4);

--GRADUATE STUDENT EDGE CASES--
INSERT INTO user_credentials VALUES
('MSmissingcore', 'missing', 5),
('MSgpa', 'gpa', 6),
('MSunder30', '30', 7),
('MSoutside2CS', '2CS', 8),
('MSbelowB', '2B', 9),
('MScleared', 'ToGraduate', 10);

--END OF user_credentials--

CREATE TABLE IF NOT EXISTS user_information(
    first_name          VARCHAR(20), 
    last_name           VARCHAR(20),
    -- sys_admin (0) /grad_sec (1) /fac_adv (2) /grad_stu (3) /alumni (4)
    type                INTEGER NOT NULL DEFAULT 5,
    email               VARCHAR(20),
    address             VARCHAR(20),
    user_id             VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES user_credentials (user_id)
);

--START OF user_information TABLE--

--DEFAULT TEST ACCOUNTS--
INSERT INTO user_information VALUES 
('admin', 'admin', 0, 'admin@gwu.edu', '123 House Ln, Washington D.C. 20001', 0),
('secretary', 'secretary', 1, 'secretary@gwu.edu', '123 House Ln, Washington D.C. 20001', 1),
('advisor', 'advisor', 2, 'advisor@gwu.edu', '123 House Ln, Washington D.C. 20001', 2),
('student', 'student', 3,'student@gwu.edu', '123 House Ln, Washington D.C. 20001', 3),
('alumni', 'alumni', 4,'alumni@gwu.edu', '123 House Ln, Washington D.C. 20001', 4);

--GRADUATE STUDENT EDGE CASES--
INSERT INTO user_information VALUES
('missing', 'core', 3, 'missingcore@gwu.edu', '123 House Ln, Washington D.C. 20001', 5),
('low', 'gpa', 3, 'toolowgpa@gwu.edu', '123 House Ln, Washington D.C. 20001', 6),
('under', '30creds', 3, 'under30creds@gwu.edu', '123 House Ln, Washington D.C. 20001', 7),
('outside', '2CS', 3, 'more2coursenotCS@gwu.edu', '123 House Ln, Washington D.C. 20001', 8),
('more2grades', 'belowB', 3, 'more2gradesbelowB@gwu.edu', '123 House Ln, Washington D.C. 20001', 9),
('can', 'graduate', 3, 'cleared2grad@gwu.edu', '123 House Ln, Washington D.C. 20001', 10);

--END OF user_information TABLE--

CREATE TABLE IF NOT EXISTS systems_administrator(
    sys_admin_id         INTEGER UNIQUE NOT NULL,
    FOREIGN KEY (sys_admin_id) REFERENCES user_credentials (user_id)
);

CREATE TABLE IF NOT EXISTS grad_secretary(
    secretary_id          INTEGER UNIQUE NOT NULL,
    FOREIGN KEY (secretary_id) REFERENCES user_credentials (user_id)
);

CREATE TABLE IF NOT EXISTS faculty_advisor(
    faculty_advisor_id     INTEGER UNIQUE NOT NULL,
    FOREIGN KEY (faculty_advisor_id) REFERENCES user_credentials (user_id)
);

INSERT INTO systems_administrator VALUES
(0);

INSERT INTO grad_secretary VALUES
(1);

INSERT INTO faculty_advisor VALUES 
(2);

CREATE TABLE IF NOT EXISTS graduate_student (
    -- student ID
    university_id       VARCHAR(20) UNIQUE,
    --user_id
    user_id             INTEGER UNIQUE,
    -- who the advisor was
    advisor_id          INTEGER,
    -- MA/MS/PhD
    type_of_program     VARCHAR(4),
    -- what they are studying
    area_of_study       VARCHAR(20),
    -- cleared for graduation, 0 is not cleared, 1 is cleared
    cleared             BIT NOT NULL DEFAULT 0,
    gpa                 VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES user_credentials (user_id),
    FOREIGN KEY (advisor_id) REFERENCES faculty_advisor (user_id)
    -- FOREIGN KEY (cleared) REFERENCES graduation_application (approved)
);


--START OF graduate_student TABLE--
INSERT INTO graduate_student VALUES
('00000000', 3, 2, 'MS', 'Computer Science', 0, '3.80'),
('00000001', 5, 2, 'MS', 'Computer Science', 0, '4.00'),
('00000002', 6, 2, 'MS', 'Computer Science', 0, '2.78'),
('00000003', 7, 2, 'MS', 'Computer Science', 0, '4.00'),
('00000004', 8, 2, 'MS', 'Computer Science', 0, '4.00'),
('00000005', 9, 2, 'MS', 'Computer Science', 0, '3.70'),
('00000006', 10, 2, 'MS', 'Computer Science', 1, '4.0');
--END OF graduate_student TABLE--

CREATE TABLE IF NOT EXISTS alumni (
    -- student ID
    university_id       VARCHAR(20) NOT NULL,
    --user_id
    user_id             INTEGER NOT NULL,
    -- year of graduation
    year_of_graduation  INT(4) NOT NULL,
    -- degree type (MA, MS, PHD)
    type_of_program     VARCHAR(4) NOT NULL,
    -- what they studied
    area_of_study       VARCHAR(20),
    -- grade point average
    gpa                 VARCHAR(20) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user_credentials (user_id)
);

--START OF alumni TABLE--
INSERT INTO alumni VALUES
('10000001', 4, 2008, 'MS', 'Computer Science','3.80');
--END OF alumni TABLE--

CREATE TABLE IF NOT EXISTS course_taken (
    university_id       VARCHAR(20) NOT NULL,
    dept                VARCHAR(4) NOT NULL,
    course_num          INT NOT NULL,
    course_title        VARCHAR(20) NOT NULL,
    credits             INT NOT NULL,
    -- freshfall (0) / freshspri (1) / sophfall (2) / sophspri (3) / jf (4) / js (5) / sf (6) / ss (7)
    semester_taken      INT NOT NULL,
    grade               VARCHAR(2)
);

--START OF course_taken TABLE--
INSERT INTO course_taken VALUES
('00000000', 'CSCI', 6221, 'SW Paradigms', 3, 4, 'A'),
('00000000', 'CSCI', 6461, 'Computer Architecture', 3, 4, 'A-'),
('00000000', 'CSCI', 6212, 'Algorithms', 3, 4, 'B+'),
('00000000', 'CSCI', 6220, 'Machine Learning', 3, 5, 'A'),
('00000000', 'CSCI', 6232, 'Networks 1', 3, 5, 'A'),
('00000000', 'CSCI', 6233, 'Networks 2', 3, 6, 'IP');
--MISSING CORE COURSES MS
INSERT INTO course_taken VALUES
('00000001', 'CSCI', 6221, 'SW Paradigms', 3, 4, 'A');
--TOO LOW GPA MS
INSERT INTO course_taken VALUES
('00000002', 'CSCI', 6221, 'SW Paradigms', 3, 4, 'A-'),
('00000002', 'CSCI', 6461, 'Computer Architecture', 3, 4, 'B-'),
('00000002', 'CSCI', 6212, 'Algorithms', 3, 4, 'C');
--NOT ENOUGH CREDITS MS
INSERT INTO course_taken VALUES
('00000003', 'CSCI', 6221, 'SW Paradigms', 3, 4, 'A'),
('00000003', 'CSCI', 6461, 'Computer Architecture', 3, 4, 'A'),
('00000003', 'CSCI', 6212, 'Algorithms', 3, 4, 'A'),
('00000003', 'CSCI', 6220, 'Machine Learning', 3, 5, 'A'),
('00000003', 'CSCI', 6232, 'Networks 1', 3, 5, 'A'),
('00000003', 'CSCI', 6241, 'Database 1', 3, 5, 'A'),
('00000003', 'CSCI', 6242, 'Database 2', 3, 5, 'A');
--MORE THAN 2 COURSES OUTSIDE CS
INSERT INTO course_taken VALUES
('00000004', 'CSCI', 6221, 'SW Paradigms', 3, 4, 'A'),
('00000004', 'CSCI', 6461, 'Computer Architecture', 3, 4, 'A'),
('00000004', 'CSCI', 6212, 'Algorithms', 3, 4, 'A'),
('00000004', 'CSCI', 6220, 'Machine Learning', 3, 5, 'A'),
('00000004', 'CSCI', 6232, 'Networks 1', 3, 5, 'A'),
('00000004', 'CSCI', 6241, 'Database 1', 3, 5, 'A'),
('00000004', 'CSCI', 6242, 'Database 2', 3, 5, 'A'),
('00000004', 'ECE', 6241, 'Communication Theory', 3, 6, 'A'),
('00000004', 'ECE', 6242, 'Information Theory', 2, 6, 'A'),
('00000004', 'MATH', 6210, 'Logic', 2, 6, 'A');
--MORE THAN 2 GRADES BELOW B
INSERT INTO course_taken VALUES
('00000005', 'CSCI', 6221, 'SW Paradigms', 3, 4, 'A'),
('00000005', 'CSCI', 6461, 'Computer Architecture', 3, 4, 'A'),
('00000005', 'CSCI', 6212, 'Algorithms', 3, 4, 'A'),
('00000005', 'CSCI', 6220, 'Machine Learning', 3, 5, 'A'),
('00000005', 'CSCI', 6232, 'Networks 1', 3, 5, 'B'),
('00000005', 'CSCI', 6241, 'Database 1', 3, 5, 'B'),
('00000005', 'CSCI', 6242, 'Database 2', 3, 5, 'A'),
('00000005', 'ECE', 6241, 'Communication Theory', 3, 6, 'B'),
('00000005', 'ECE', 6242, 'Information Theory', 2, 6, 'A'),
('00000005', 'MATH', 6210, 'Logic', 2, 6, 'A');
--CLEARED TO GRADUATE
INSERT INTO course_taken VALUES
('00000006', 'CSCI', 6221, 'SW Paradigms', 3, 4, 'A'),
('00000006', 'CSCI', 6461, 'Computer Architecture', 3, 4, 'A'),
('00000006', 'CSCI', 6212, 'Algorithms', 3, 4, 'A'),
('00000006', 'CSCI', 6220, 'Machine Learning', 3, 4, 'A'),
('00000006', 'CSCI', 6232, 'Networks 1', 3, 4, 'A'),
('00000006', 'CSCI', 6233, 'Networks 2', 3, 4, 'A'),
('00000006', 'CSCI', 6241, 'Database 1', 3, 4, 'A'),
('00000006', 'CSCI', 6242, 'Database 2', 3, 4, 'A'),
('00000006', 'CSCI', 6246, 'Compilers', 3, 4, 'A'),
('00000006', 'CSCI', 6260, 'Multimedia', 3, 4, 'A'),
('00000006', 'CSCI', 6251, 'Cloud Computing', 3, 4, 'A'),
('00000006', 'CSCI', 6254, 'SW Engineering', 3, 4, 'A');
--ALUMNI TEST
INSERT INTO course_taken VALUES
('00000007', 'CSCI', 6221, 'SW Paradigms', 3, 4, 'A');
--END OF course_taken TABLE--

CREATE TABLE IF NOT EXISTS course (
    dept                VARCHAR(4) NOT NULL,
    course_num          INT NOT NULL,
    course_title        VARCHAR(20) NOT NULL,
    credits             INT NOT NULL
);

CREATE TABLE IF NOT EXISTS prerequisite (
    dept_prereq         VARCHAR(4),
    dept                VARCHAR(4) NOT NULL,
    course_num_prereq   INT,
    course_num          INT NOT NULL,
    FOREIGN KEY (dept) REFERENCES course (dept),
    FOREIGN KEY (dept_prereq) REFERENCES course (dept),
    FOREIGN KEY (course_num) REFERENCES course (course_num),
    FOREIGN KEY (course_num_prereq) REFERENCES course (course_num)
);
CREATE TABLE IF NOT EXISTS thesis (
    form_id                            INTEGER PRIMARY KEY AUTOINCREMENT,
    thesis                             TEXT,
    submitted_university_id            VARCHAR(20) NOT NULL,
    FOREIGN KEY (submitted_university_id) REFERENCES graduate_student (university_id),  
    FOREIGN KEY (form_id) REFERENCES forms (form_id)
);
CREATE TABLE IF NOT EXISTS forms (
    form_id                            INTEGER PRIMARY KEY AUTOINCREMENT,
    submitted_university_id            VARCHAR(20) NOT NULL,
    approved                           BIT DEFAULT 0,
    FOREIGN KEY (submitted_university_id) REFERENCES graduate_student (university_id)
);
CREATE TABLE IF NOT EXISTS graduation_application (
    form_id                            INTEGER PRIMARY KEY AUTOINCREMENT,
    submitted_university_id            VARCHAR(20) NOT NULL,
    approved                           BIT DEFAULT 0,
    FOREIGN KEY (submitted_university_id) REFERENCES graduate_student (university_id)
);
CREATE TABLE IF NOT EXISTS forms_classes (
    form_id             INTEGER,
    university_id       VARCHAR(20) NOT NULL,
    dept                VARCHAR(4) NOT NULL,
    course_num          INT NOT NULL,
    FOREIGN KEY (dept) REFERENCES course (dept),
    FOREIGN KEY (course_num) REFERENCES course (course_num)
);
CREATE TABLE IF NOT EXISTS program (
    program_id INT NOT NULL,
    program_field VARCHAR(20) NOT NULL,
    program_degree VARCHAR(4) NOT NULL,
    program_gpa_min FLOAT NOT NULL,
    credit_hrs INT NOT NULL,
    -- neccessary credits in program
    credit_hrs_prgm INT NOT NULL,
    -- most courses outside of program that will count towards degree
    courses_non_prgm INT NOT NULL,
    below_b INT NOT NULL,
    thesis BIT NOT NULL
);

INSERT INTO program VALUES 
(0, 'CSCI', 'MS', 3.0, 30, 0, 2, 2, 0),
(1, 'CSCI', 'PhD', 3.5, 36, 30, 6, 1, 1);

-- Inserting courses into the course table
INSERT INTO course VALUES
('CSCI', 6221, 'SW Paradigms', 3),
('CSCI', 6461, 'Computer Architecture', 3),
('CSCI', 6212, 'Algorithms', 3),
('CSCI', 6220, 'Machine Learning', 3),
('CSCI', 6232, 'Networks 1', 3),
('CSCI', 6233, 'Networks 2', 3),
('CSCI', 6241, 'Database 1', 3),
('CSCI', 6242, 'Database 2', 3),
('CSCI', 6246, 'Compilers', 3),
('CSCI', 6260, 'Multimedia', 3),
('CSCI', 6251, 'Cloud Computing', 3),
('CSCI', 6254, 'SW Engineering', 3),
('CSCI', 6262, 'Graphics 1', 3),
('CSCI', 6283, 'Security 1', 3),
('CSCI', 6284, 'Cryptography', 3),
('CSCI', 6286, 'Network Security', 3),
('CSCI', 6325, 'Algorithms 2', 3),
('CSCI', 6339, 'Embedded Systems', 3),
('CSCI', 6384, 'Cryptography 2', 3),
('ECE', 6241, 'Communication Theory', 3),
('ECE', 6242, 'Information Theory', 2),
('MATH', 6210, 'Logic', 2);

-- Inserting courses into the prerequisite table
INSERT INTO prerequisite VALUES
('CSCI', 6232, 'CSCI', 6233),
('CSCI', 6241, 'CSCI', 6242),
('CSCI', 6461, 'CSCI', 6246),
('CSCI', 6212, 'CSCI', 6246),
('CSCI', 6461, 'CSCI', 6251),
('CSCI', 6221, 'CSCI', 6254),
('CSCI', 6212, 'CSCI', 6283),
('CSCI', 6212, 'CSCI', 6284),
('CSCI', 6283, 'CSCI', 6286),
('CSCI', 6232, 'CSCI', 6286),
('CSCI', 6212, 'CSCI', 6325),
('CSCI', 6461, 'CSCI', 6339),
('CSCI', 6212, 'CSCI', 6339),
('CSCI', 6284, 'CSCI', 6384);


DROP TABLE IF EXISTS MS_requirements;
DROP TABLE IF EXISTS MS_required_courses;

DROP TABLE IF EXISTS PhD_requirements;
DROP TABLE IF EXISTS PhD_required_courses;

CREATE TABLE IF NOT EXISTS MS_requirements(
    min_gpa                         VARCHAR(20),
    min_credit_hours                INTEGER,
    most_courses_outside_CS         INTEGER,
    most_grades_below_B               INTEGER
);

--START OF MS_requirements TABLE--
INSERT INTO MS_requirements VALUES
('3.0', 30, 2, 2);
--END OF MS_requirements TABLE--

CREATE TABLE IF NOT EXISTS MS_required_courses(
    dept                VARCHAR(4) NOT NULL,
    course_num          INT NOT NULL,
    course_title        VARCHAR(20) NOT NULL,
    credits             INT NOT NULL
);

--START OF MS_required_courses TABLE--
INSERT INTO MS_required_courses VALUES
('CSCI', 6221, 'SW Paradigms', 3),
('CSCI', 6212, 'Algorithms', 3),
('CSCI', 6461, 'Computer Architecture', 3);
--END OF MS_required_courses TABLE--

CREATE TABLE IF NOT EXISTS PhD_requirements(
    min_gpa                         VARCHAR(20),
    min_credit_hours                INTEGER,
    min_credits_in_cs               INTEGER,
    most_grades_below_B             INTEGER,
    pass_thesis_Defense             BIT NOT NULL DEFAULT 0
);

--START OF PhD_requirements TABLE--
INSERT INTO PhD_requirements VALUES
('3.5', 36, 30, 1, 0);
--END OF PhD_requirements TABLE--

CREATE TABLE IF NOT EXISTS PhD_required_courses(
    dept                VARCHAR(4) NOT NULL,
    course_num          INT NOT NULL,
    course_title        VARCHAR(20) NOT NULL,
    credits             INT NOT NULL
);

--START OF PhD_required_courses TABLE--
INSERT INTO PhD_required_courses VALUES
('CSCI', 6221, 'SW Paradigms', 3),
('CSCI', 6212, 'Algorithms', 3),
('CSCI', 6461, 'Computer Architecture', 3);
--END OF PhD_required_courses TABLE--





--DEMO TEST STARTING STATE--

--McCartney, Paul--
INSERT INTO user_credentials (user, pass, user_id) 
VALUES ('pauluser', 'paulpass', 11);
INSERT INTO user_information (first_name, last_name, type, email, address, user_id)
VALUES ('Paul', 'McCartney', 3, 'pmc@gwu.edu', 'J William Fullbright Hall', 11);
INSERT INTO graduate_student (university_id, user_id, advisor_id, type_of_program, area_of_study, cleared, gpa)
VALUES ('55555555', 11, 16, 'MS', 'Computer Science', 0, '3.5');
INSERT INTO course_taken (university_id, dept, course_num, course_title, credits, semester_taken, grade)
VALUES ('55555555', 'CSCI', 6221, 'SW Paradigms', 3, 4, 'A'),
('55555555', 'CSCI', 6212, 'Algorithms', 3, 4, 'A'),
('55555555', 'CSCI', 6461, 'Computer Architecture', 3, 4, 'A'),
('55555555', 'CSCI', 6232, 'Networks 1', 3, 4, 'A'),
('55555555', 'CSCI', 6233, 'Networks 2', 3, 4, 'A'),
('55555555', 'CSCI', 6241, 'Database 1', 3, 4, 'B'),
('55555555', 'CSCI', 6246, 'Compilers', 3, 4, 'B'),
('55555555', 'CSCI', 6262, 'Graphics 1', 3, 4, 'B'),
('55555555', 'CSCI', 6283, 'Security 1', 3, 4, 'B'),
('55555555', 'CSCI', 6242, 'Database 2', 3, 4, 'B');

--Harrison, George--
INSERT INTO user_credentials (user, pass, user_id) 
VALUES ('georgeuser', 'georgepass', 12);
INSERT INTO user_information (first_name, last_name, type, email, address, user_id)
VALUES ('George', 'Harrison', 3, 'gh@gwu.edu', 'J William Fullbright Hall', 12);
INSERT INTO graduate_student (university_id, user_id, advisor_id, type_of_program, area_of_study, cleared, gpa)
VALUES ('66666666', 12, 17, 'MS', 'Computer Science', 0, '2.9');
INSERT INTO course_taken (university_id, dept, course_num, course_title, credits, semester_taken, grade)
VALUES ('66666666', 'ECE', 6242, 'Information Theory', 3, 4, 'C'),
('66666666', 'CSCI', 6221, 'SW Paradigms', 3, 4, 'B'),
('66666666', 'CSCI', 6461, 'Computer Architecture', 3, 4, 'B'),
('66666666', 'CSCI', 6212, 'Algorithms', 3, 4, 'B'),
('66666666', 'CSCI', 6232, 'Networks 1', 3, 4, 'B'),
('66666666', 'CSCI', 6233, 'Networks 2', 3, 4, 'B'),
('66666666', 'CSCI', 6241, 'Database 1', 3, 4, 'B'),
('66666666', 'CSCI', 6242, 'Database 2', 3, 4, 'B'),
('66666666', 'CSCI', 6283, 'Security 1', 3, 4, 'B'),
('66666666', 'CSCI', 6284, 'Cryptography', 3, 4 , 'B');

--Starr, Ringo--
INSERT INTO user_credentials (user, pass, user_id) 
VALUES ('ringouser', 'ringopass', 13);
INSERT INTO user_information (first_name, last_name, type, email, address, user_id)
VALUES ('Ringo', 'Starr', 3, 'rs@gwu.edu', 'SEAS', 13);
INSERT INTO graduate_student (university_id, user_id, advisor_id, type_of_program, area_of_study, cleared, gpa)
VALUES ('12345678', 13, 17, 'PhD', 'Computer Science', 0, '4.0');
INSERT INTO course_taken (university_id, dept, course_num, course_title, credits, semester_taken, grade)
VALUES ('12345678', 'CSCI', 6221, 'SW Paradigms', 3, 4, 'A'),
('12345678', 'CSCI', 6461, 'Computer Architecture', 3, 4, 'A'),
('12345678', 'CSCI', 6212, 'Algorithms', 3, 4, 'A'),
('12345678', 'CSCI', 6220, 'Machine Learning', 3, 4, 'A'),
('12345678', 'CSCI', 6232, 'Networks 1', 3, 4, 'A'),
('12345678', 'CSCI', 6233, 'Networks 2', 3, 4, 'A'),
('12345678', 'CSCI', 6241, 'Database 1', 3, 4, 'A'),
('12345678', 'CSCI', 6242, 'Database 2', 3, 4, 'A'),
('12345678', 'CSCI', 6246, 'Compilers', 3, 4, 'A'),
('12345678', 'CSCI', 6260, 'Multimedia', 3, 4, 'A'),
('12345678', 'CSCI', 6251, 'Cloud Computing', 3, 4, 'A'),
('12345678', 'CSCI', 6254, 'SW Engineering', 3, 4, 'A');

--Clapton, Eric--
INSERT INTO user_credentials (user, pass, user_id) 
VALUES ('ericuser', 'ericpass', 14);
INSERT INTO user_information (first_name, last_name, type, email, address, user_id)
VALUES ('Eric', 'Clapton', 4, 'ec@gwu.edu', '123 House in Chicago', 14);
INSERT INTO alumni (university_id, user_id, year_of_graduation, type_of_program, area_of_study, gpa)
VALUES ('77777777', 14, 2014, 'MS', 'Computer Science', '3.3');
INSERT INTO course_taken (university_id, dept, course_num, course_title, credits, semester_taken, grade)
VALUES ('77777777', 'CSCI', 6221, 'SW Paradigms', 3, 4, 'B'),
('77777777', 'CSCI', 6461, 'Computer Architecture', 3, 4, 'B'),
('77777777', 'CSCI', 6212, 'Algorithms', 3, 4, 'B'),
('77777777', 'CSCI', 6232, 'Networks 1', 3, 4, 'B'),
('77777777', 'CSCI', 6233, 'Networks 2', 3, 4, 'B'),
('77777777', 'CSCI', 6241, 'Database 1', 3, 5, 'B'),
('77777777', 'CSCI', 6242, 'Database 2', 3, 5, 'B'),
('77777777', 'CSCI', 6283, 'Security 1', 3, 6, 'A'),
('77777777', 'CSCI', 6284, 'Cryptography', 3, 6, 'A'),
('77777777', 'CSCI', 6286, 'Network Security', 3, 6, 'A');

--Perry, Katy--
INSERT INTO user_credentials (user, pass, user_id) 
VALUES ('katyuser', 'katypass', 15);
INSERT INTO user_information (first_name, last_name, type, email, address, user_id)
VALUES ('Katy', 'Perry', 1, 'kp@gwu.edu', '9570 Hidden Valley Road, Beverly Hills, California', 15);
INSERT INTO grad_secretary (secretary_id) VALUES
(15);

--Narahari, Bhagirath--
INSERT INTO user_credentials (user, pass, user_id) 
VALUES ('narahariuser', 'naraharipass', 16);
INSERT INTO user_information (first_name, last_name, type, email, address, user_id)
VALUES ('Bhagirath', 'Narahari', 2, 'bn@gwu.edu', 'SEAS', 16);
INSERT INTO faculty_advisor (faculty_advisor_id) VALUES
(16);

--Parmer , Gabriel--
INSERT INTO user_credentials (user, pass, user_id) 
VALUES ('parmeruser', 'parmerpass', 17);
INSERT INTO user_information (first_name, last_name, type, email, address, user_id)
VALUES ('Gabriel', 'Parmer', 2, 'gp@gwu.edu', 'SEAS', 17);
INSERT INTO faculty_advisor (faculty_advisor_id) VALUES
(17);