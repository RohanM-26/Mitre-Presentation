README.md

This application has a ton of dependencies

If you are on a linux machine you must setup the virtual environment. Follow these steps

python3 -m venv venv_directory
source venv_directory/bin/activate


pip install -r requirements.txt

To run the code:

python main.py




The main goal of this project is to create an advising program where sutdents will "apply to graduate"


'''
from requirements.txt
'''



ADS workflow:
You must implement the workflow below. For specific data needed for this component, refer to
the information below as well as your analysis of what other data may be required.
● Each graduate student should be able to create an account that enables them to log into
the system.
● A graduate student has personal information that identifies them.
o Each student has a unique university ID (UID) which is an 8 digit number.
o The system must store the last and first name of the student, and other personal
information such as address.
o A student can be enrolled in the Masters program or the PhD program; the
system must store this information.
o A graduate student in the university is assigned a faculty advisor by the GS.
o The system must be able to provide a login for each student in the university.
● We assume that the student has taken some courses, and the system stores course
enrollment information for each student. This information includes courses taken by the
student, the semester and year taken, the final grade for the course (if completed),
number of credit hours. In other words, information that is typically found on a
transcript.
● A student must specify their entire program of study plan by filling out a Form 1 and
having a faculty advisor view the form. This lists the courses that they will take to meet
the Degree requirements (this is somewhat similar to the curriculum sheets that
undergraduates must follow to meet their degree requirements.). A sample of a Form 1
is provided in the Appendix in this document.
● After completing the requirements for the degree to which they are admitted, the
student formally applies for graduation by visiting the “Apply for Graduation” portion of
the website, and selecting the degree to which they are applying. If you want to make a
simplifying assumption for Phase 1, at risk of losing some points, then assume students
are only applying for the MS degree.
● Since you will need to look up their enrollment information (transcript), assume that
they have taken courses only from the course catalog provided in this document (in the
Appendix.
o Assume that the valid final grades are (A, A-, B+, B, B-, C+, C, F).Courses currently
in progress show up with a grade of IP (in progress).
● Once a student has applied for graduation, the system automatically performs an
‘audit’. Specifically the system checks to see if the student has satisfied all the degree
program requirements:
o This requires that the system check the courses the student has taken and
compare them with the program requirements (both course requirements and
GPA requirements) and compares them with the courses the student listed on
their Form 1. (For example, if they have taken a different set of courses thanlisted on their Form 1 then they will not be cleared for graduation). You could
simplify the process by checking for program requirements when they submit
their Form 1 -- i.e., check if the courses listed on their Form 1 meet the course
requirements of the MS program; thus, the application for graduation will only
test if they have filed a Form 1 and if they satisfy the GPA rule.
o If you want to simplify the project in Phase 1 (at the risk of losing 10% of the
points), assume that only MS students will apply for graduation. The program
requirements for both the MS and PhD are provided in the appendix.
o In general, program requirements for the degree (e.g., required courses for the
MS degree) should be stored in the database. This will allow changes to the
program requirements to be made without code modifications.
● Once a student is cleared for graduation by passing the audit, the GS formally process
their application and they “graduate”. Note that a student can be cleared for graduation
but they do not actually graduate until the GS, or another authorized user, enters this
information into the system and formally clears them.
o The process of graduation must be automated; i.e., the GS need only check the
“cleared for graduation” students and approve their graduation by clicking on
some selection. (In practice the GS actually looks through their folder and
transcript, and their accounts payable balance.)
● When a student “graduates” they are removed from the Graduate student table and
their information must be entered into an Alumni table. Note that only a summary of
their academic information should be kept in the Alumni table.
o In a real system, the enrollment information for a student is not removed since
they may re-enroll at GWU for another degree. Thus, a graduation process would
only require that their data be tagged to indicate that they have graduated with a
degree while keeping all their information intact.
● An alumni can only edit their personal information (such as email, address) and view
their transcript.






Users and Roles:
Observe that there are different categories of users of the ADS system, and each type of user
has specific roles and authorizations.
● Systems administrator
o Has access to everything and must create the different types of user accounts
● Grad Secretary (GS)
o Has complete access to current student’s data. They are responsible for
assigning an advisor and for graduating a student. Note that they cannot create
new users.
● Faculty advisors
o These are faculty in the department and can review Form 1; for PhD students
they have to approve (pass) the PhD thesis.
o They can view their advisees’ transcript but cannot update the transcript. This is
the only access they are given.
● Graduate Students
o They can view their enrollment information (such as courses taken and grades)
but cannot update their grades. They enter the Form1 data, and can apply for
graduation. They can update their personal information (address, email etc.) but
no other information.
● Alumni: They can log into the system and edit their personal information only.