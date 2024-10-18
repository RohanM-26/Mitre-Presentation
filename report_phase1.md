# Phase I Report


# General

We are ADS, our 'mentor' is Dania.

## Entity-Relation Diagram

> Please provide an ER diagram for your DB organization.

![ER Diagram](static/ER.png)

## DB Organization

> Please provide documentation for your chosen data-base schema, including a discussion of the normalization levels.


user_credentials Table

- **Attributes:**
  - user: VARCHAR(20) (Primary Key)
  - pass: VARCHAR(20)
  - user_id: INTEGER (Unique)

- This table satisfies 1NF, 2NF, and 3NF, primary key is user_id and it gives all attributes.

user_information Table

- **Attributes:**
  - first_name: VARCHAR(20)
  - last_name: VARCHAR(20)
  - type: INTEGER (Default: 5)
  - email: VARCHAR(20)
  - address: VARCHAR(20)
  - user_id: VARCHAR(20) (Foreign Key)

- This table satisfies 1NF, 2NF, and 3NF, primary key is user_id and it gives all other fields, email is not a primary keys one person may have different roles.

systems_administrator Table

- **Attributes:**
  - sys_admin_id: INTEGER (Unique)

- This table satisfies 1NF, 2NF, and 3NF, there is only one attribute so far, this table may see more as needed though.

grad_secretary Table

- **Attributes:**
  - secretary_id: INTEGER (Unique)

  - This table satisfies 1NF, 2NF, and 3NF, there is only one attribute so far, this table may see more as needed though.

faculty_advisor Table

- **Attributes:**
  - faculty_advisor_id: INTEGER (Unique)

- This table satisfies 1NF, 2NF, and 3NF, there is only one attribute so far, this table may see more as needed though.

graduate_student Table

- **Attributes:**
  - university_id: VARCHAR(20) (Primary Key)
  - user_id: INTEGER (Unique, Foreign Key)
  - advisor_id: INTEGER (Foreign Key)
  - type_of_program: VARCHAR(4)
  - area_of_study: VARCHAR(20)
  - cleared: BIT (Default: 0)
  - gpa: VARCHAR(20)

- This table satisfies 1NF, as university_id and user_id are superkeys and determine all other fields.

alumni Table

- **Attributes:**
  - university_id: VARCHAR(20)
  - user_id: INTEGER
  - year_of_graduation: INT(4)
  - gpa: VARCHAR(20)
  - type_of_program: VARCHAR(4)
  - area_of_study: VARCHAR(20)

- This table satisfies 1NF, 2NF, and 3NF, as university_id and user_id are superkeys and determine all other fields.

course_taken Table

- **Attributes:**
  - university_id: VARCHAR(20)
  - dept: VARCHAR(4)
  - course_num: INT
  - course_title: VARCHAR(20)
  - credits: INT
  - semester_taken: INT
  - grade: VARCHAR(2)

- This table satisfies 1NF, as university_id, dept, and course_num is a superkey but dept and course_num determine credits and title.

course Table

- **Attributes:**
  - dept: VARCHAR(4) (Primary Key)
  - course_num: INT (Primary Key)
  - course_title: VARCHAR(20)
  - credits: INT

- This table satisfies 1NF, 2NF, and 3NF, the primary key dept and course_num determine all fields.

prerequisite Table

- **Attributes:**
  - dept_prereq: VARCHAR(4)
  - dept: VARCHAR(4)
  - course_num_prereq: INT
  - course_num: INT

- This table satisfies 1NF, 2NF, and 3NF, as all elements are part of the primary key.

forms Table

- **Attributes:**
  - form_id: INTEGER (Primary Key)
  - submitted_university_id: VARCHAR(20)
  - approved: BIT (Default: 0)

- This table satisfies 1NF, 2NF, and 3NF, as form_id, and only form_id, determine the other fields.

thesis Table

- **Attributes:**
  - form_id: INTEGER (Primary Key)
  - thesis: TEXT
  - submitted_university_id: VARCHAR(20)

- This table satisfies 1NF, 2NF, and 3NF, as only form_id (primary key) determines the other fields.

forms_classes Table

- **Attributes:**
  - form_id: VARCHAR(20)
  - dept: VARCHAR(4)
  - course_num: INT

- This table satisfies 1NF, 2NF, and 3NF, all elements are in the primary key.

program Table

- **Attributes:**
  - program_id: INT
  - program_field: VARCHAR(20)
  - program_degree: VARCHAR(4)
  - program_gpa_min: FLOAT
  - credit_hrs: INT
  - credit_hrs_prgm: INT
  - courses_non_prgm: INT
  - below_b: INT
  - thesis: BIT

- This table satisfies 1NF, 2NF, and 3NF, all elements can be determined by the id or field and degree, which are superkeys.

MS_requirements Table

- **Attributes:**
  - min_gpa: VARCHAR(20)
  - min_credit_hours: INTEGER
  - most_courses_outside_CS: INTEGER
  - most_grades_below_B: INTEGER

- This table satisfies 1NF, 2NF, and 3NF, as the primary key is all values, 

MS_required_courses Table

- **Attributes:**
  - dept: VARCHAR(4)
  - course_num: INT
  - course_title: VARCHAR(20)
  - credits: INT

- This table satisfies 1NF, 2NF, and 3NF, as the primary key is all values, and there is one entry. 

PhD_requirements Table

- **Attributes:**
  - min_gpa: VARCHAR(20)
  - min_credit_hours: INTEGER
  - min_credits_in_cs: INTEGER
  - most_grades_below_B: INTEGER
  - pass_thesis_Defense: BIT (Default: 0)

- This table satisfies 1NF, 2NF, and 3NF, as the primary key is all values, and there is one entry.

PhD_required_courses Table

- **Attributes:**
  - dept: VARCHAR(4)
  - course_num: INT
  - course_title: VARCHAR(20)
  - credits: INT

- This table satisfies 1NF, 2NF, and 3NF, as the primary key is all values, and there is one entry.

## Testing

> Please detail and document how you test the system. Separately document any unit tests, and manual tests.

> For testing we mainly manually tested each user before commiting the changes making sure everything worked smoothly
> especially for random cases where there is user error since that is very common when it comes to websites like these.
> We had no unit tests except we had print statements for debugging to make sure each and every input followed the flow
> we wanted it to follow i.e If you click a tab we would have a print statement so that we knew that the website
> redirected the user to the correct page. We also had error messages so something invalid wouldn't happen like someone
> getting approved for graduation when they shouldn't have been. We didn't think we needed Unit Tests because it is a
> website but upon further inspection it will not hurt and we will make sure to implement them in our final design.
> We plan to implement some unit tests that will make sure the database updates accordingly when someone graduates
> taking them out of the student system and putting them into the alumni system.


LOGIN INFORMATION FOR DEMO DAY

--McCartney, Paul--
'pauluser', 'paulpass'

--Harrison, George--
'georgeuser', 'georgepass'

--Starr, Ringo--
'ringouser', 'ringopass'

--Clapton, Eric--
'ericuser', 'ericpass'

--Perry, Katy--
'katyuser', 'katypass'

--Narahari, Bhagirath--
'narahariuser','naraharipass'

--Parmer , Gabriel--
'parmeruser', 'parmerpass'

GS - 'secretaryuser', 'secretarypass'
Admin - 'adminuser', 'adminpass'
