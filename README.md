Student Grade Management System

>> About the Project

This is the implementation of a simple Student Grade Management System created using Python.

The project is created in order to store and manage the student's data including their name, roll number, and marks, while also calculating the percentage and grade automatically.

The program has a nice graphical interface, from which you can add, edit, delete and search for students by their name or roll number, view all students, and calculate percentage, grade, number of students, average percentage, passed students, and failed students automatically.



Q. What Can We Do With This Project?

With this program, we can:

Add a new student, save students' data, edit students' data, delete a student's data, search for a student, view all students, calculate percentage automatically, calculate grade automatically, view the total number of students, view the average percentage, view the number of passed students and failed students.



Q. How Are Grades Given?

Grades are given based on the marks:

| Marks |    | Grade |


 90-100         A+ 

 80-89          A 

 70-79          B+ 

 60-69          B 

 50-59          C 

 40-49          D 

 below 40       F 

A student scoring 40 or above is considered to have passed the exam.



Q. What Was Used to Make This Project?

The project basically used:

Python – to write the Python program

Tkinter – to create the application's windows, buttons, and tables

JSON – to store the student's data

No additional Python libraries are required.



>> Files in the Project

text

student_grade_manager.py

students_data.json

README.md


>> student_grade_manager.py

This is the file containing the Python program implementing the application.

>> students_data.json

This is the file that stores data of the students.

This file is created automatically when students are saved into the application.

>> README.md

This is the file being read right now; this file explains the project.



Q. How to Run This Project

>> Using Python IDLE

1. Open Python IDLE.

2. Open the file `student_grade_manager.py`.

3. Click F5.

4. The application window will open.

That's it.

Alternatively, you can also run the application using the Command Prompt with the following command:

text

python student_grade_manager.py





Q. How to Add a Student

Enter:

The student's name

The student's roll number

The student's marks

 and click Save Student.

The program will automatically calculate the percentage and grade and display the student in the table.



Q. How to Edit a Student

Select a student from the table.

The student's details will appear in the input fields upon double-clicking the selected student.

Change the desired information and click Edit.



Q. How to Delete a Student

Select the student you want to delete.

Click Delete Selected Student.

The program will prompt a message asking if you want to confirm the deletion.



Q. How to Search

Enter the student's name or roll number in the search input field and click Search.

To view all students, click Show All.



>> Saving Data

Student data is stored in the following file:

text

students_data.json



This ensures that the data will stay on your computer even when the application is closed.

When you reopen the application, the previously stored students will be displayed automatically.



>> Some Checks in the Program

The application also performs some basic checks.

For example, it will not allow you to:

Have an empty name

Have an empty roll number

Have a mark that is not in between 0 and 100

Have a mark that is not a number

Have two students with the same roll number



>> Dashboard

On the top of the application window, there is a small dashboard displaying:

Total students

Average percentage

Passed students

Failed students

All of these values update automatically whenever any changes are made to the student records.



Q. Why I Made This Project

I made this project in order to learn how to use Python to create a simple real-world application.

In the process, I had the opportunity to practice various Python features including:

Functions

Lists

Dictionaries

If-else statements

Loops

File handling

Tkinter

Saving and loading data



>> Future Improvements

Some additional features that can be added to this application in the future include:

Subjects

Attendance

Student photos

PDF reports

Excel reports

Login system

Improved performance charts

Database support



>> Conclusion

This project is a simple student management application built using Python.

This project allows us to easily store student data including their name, roll number, and marks, and calculate their grade automatically.

All of this is possible with just one simple application.



 Author

Name: Himanshu Vinchurkar

Course: B.Tech Aerospace Engineering

College: VIT Bhopal University

Project: Student Grade Management System
