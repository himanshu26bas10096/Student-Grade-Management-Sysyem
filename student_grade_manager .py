import tkinter as tk
from tkinter import ttk, messagebox
import json
import os



# SETTINGS


DATA_FILE = "students_data.json"



# STUDENT DATA


students = []


def load_data():
    """Load saved students from the data file."""

    global students

    if not os.path.exists(DATA_FILE):
        students = []
        return

    try:
        with open(DATA_FILE, "r") as file:
            students = json.load(file)

        if not isinstance(students, list):
            students = []

    except:
        students = []


def save_data():
    """Save all students to the data file."""

    try:
        with open(DATA_FILE, "w") as file:
            json.dump(students, file, indent=4)

        return True

    except Exception as error:
        messagebox.showerror(
            "Save Error",
            "Student data could not be saved.\n\n" + str(error)
        )

        return False



# GRADE CALCULATION


def calculate_grade(marks):

    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B+"
    elif marks >= 60:
        return "B"
    elif marks >= 50:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "F"



# INPUT FUNCTIONS


def clear_fields():

    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)

    name_entry.focus()


def get_input():

    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    marks_text = marks_entry.get().strip()

    if name == "":
        messagebox.showwarning(
            "Missing Information",
            "Please enter the student's name."
        )
        return None

    if roll == "":
        messagebox.showwarning(
            "Missing Information",
            "Please enter the roll number."
        )
        return None

    if marks_text == "":
        messagebox.showwarning(
            "Missing Information",
            "Please enter the marks."
        )
        return None

    try:
        marks = float(marks_text)
    except ValueError:
        messagebox.showwarning(
            "Invalid Marks",
            "Marks must be a number."
        )
        return None

    if marks < 0 or marks > 100:
        messagebox.showwarning(
            "Invalid Marks",
            "Marks must be between 0 and 100."
        )
        return None

    return name, roll, marks



# ADD STUDENT

def add_student():

    data = get_input()

    if data is None:
        return

    name, roll, marks = data

    # Check duplicate roll number
    for student in students:

        if student["roll"] == roll:

            messagebox.showwarning(
                "Duplicate Roll Number",
                "A student with this roll number already exists."
            )

            return

    percentage = marks
    grade = calculate_grade(percentage)

    student = {
        "name": name,
        "roll": roll,
        "marks": marks,
        "percentage": percentage,
        "grade": grade
    }

    students.append(student)

    # THIS IS THE IMPORTANT SAVE STEP
    if save_data():

        refresh_table()
        update_dashboard()
        clear_fields()

        messagebox.showinfo(
            "Saved",
            "Student saved successfully!"
        )



# EDIT STUDENT


def edit_student():

    selected = student_table.selection()

    if not selected:

        messagebox.showwarning(
            "No Student Selected",
            "Please select a student from the table."
        )

        return

    data = get_input()

    if data is None:
        return

    name, new_roll, marks = data

    item = selected[0]

    values = student_table.item(
        item,
        "values"
    )

    old_roll = values[1]

    # Check duplicate roll number
    for student in students:

        if (
            student["roll"] == new_roll
            and student["roll"] != old_roll
        ):

            messagebox.showwarning(
                "Duplicate Roll Number",
                "Another student already has this roll number."
            )

            return

    # Find and update student
    for student in students:

        if student["roll"] == old_roll:

            student["name"] = name
            student["roll"] = new_roll
            student["marks"] = marks
            student["percentage"] = marks
            student["grade"] = calculate_grade(marks)

            break

    if save_data():

        refresh_table()
        update_dashboard()
        clear_fields()

        messagebox.showinfo(
            "Updated",
            "Student information updated successfully!"
        )



# DELETE STUDENT


def delete_student():

    selected = student_table.selection()

    if not selected:

        messagebox.showwarning(
            "No Student Selected",
            "Please select a student first."
        )

        return

    item = selected[0]

    values = student_table.item(
        item,
        "values"
    )

    roll = values[1]

    answer = messagebox.askyesno(
        "Delete Student",
        "Are you sure you want to delete this student?"
    )

    if not answer:
        return

    for student in students:

        if student["roll"] == roll:

            students.remove(student)
            break

    if save_data():

        refresh_table()
        update_dashboard()
        clear_fields()

        messagebox.showinfo(
            "Deleted",
            "Student deleted successfully!"
        )



# SELECT STUDENT


def select_student(event=None):

    selected = student_table.selection()

    if not selected:
        return

    item = selected[0]

    values = student_table.item(
        item,
        "values"
    )

    clear_fields()

    name_entry.insert(
        0,
        values[0]
    )

    roll_entry.insert(
        0,
        values[1]
    )

    marks_entry.insert(
        0,
        values[2]
    )



# TABLE


def add_to_table(student):

    grade = student["grade"]

    item = student_table.insert(
        "",
        tk.END,
        values=(
            student["name"],
            student["roll"],
            student["marks"],
            f"{float(student['percentage']):.2f}%",
            grade
        )
    )

    # Color the grade text
    if grade in ("A+", "A"):
        student_table.item(
            item,
            tags=("excellent",)
        )

    elif grade in ("B+", "B"):
        student_table.item(
            item,
            tags=("good",)
        )

    elif grade in ("C", "D"):
        student_table.item(
            item,
            tags=("average",)
        )

    else:
        student_table.item(
            item,
            tags=("failed",)
        )


def refresh_table():

    for item in student_table.get_children():
        student_table.delete(item)

    for student in students:
        add_to_table(student)



# SEARCH


def search_student():

    search_text = search_entry.get().strip().lower()

    for item in student_table.get_children():
        student_table.delete(item)

    if search_text == "":
        refresh_table()
        return

    for student in students:

        name = student["name"].lower()
        roll = student["roll"].lower()

        if search_text in name or search_text in roll:
            add_to_table(student)


def show_all():

    search_entry.delete(
        0,
        tk.END
    )

    refresh_table()



# DASHBOARD


def update_dashboard():

    total = len(students)

    if total == 0:

        average = 0
        passed = 0
        failed = 0

    else:

        total_marks = 0
        passed = 0
        failed = 0

        for student in students:

            marks = float(
                student["percentage"]
            )

            total_marks += marks

            if marks >= 40:
                passed += 1
            else:
                failed += 1

        average = total_marks / total

    total_label.config(
        text=str(total)
    )

    average_label.config(
        text=f"{average:.1f}%"
    )

    passed_label.config(
        text=str(passed)
    )

    failed_label.config(
        text=str(failed)
    )



# MAIN WINDOW


root = tk.Tk()

root.title(
    "Student Grade Management System"
)

root.geometry(
    "1050x700"
)

root.minsize(
    900,
    600
)

root.configure(
    bg="#eef2f7"
)



# STYLE


style = ttk.Style()

try:
    style.theme_use("clam")
except:
    pass


style.configure(
    "Treeview",
    background="white",
    foreground="#222222",
    rowheight=36,
    fieldbackground="white",
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background="#243447",
    foreground="white",
    font=("Segoe UI", 10, "bold"),
    padding=8
)

style.map(
    "Treeview",
    background=[
        ("selected", "#dbeafe")
    ],
    foreground=[
        ("selected", "#111827")
    ]
)



# HEADER


header = tk.Frame(
    root,
    bg="#243447",
    height=90
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


tk.Label(
    header,
    text="STUDENT GRADE MANAGER",
    font=("Segoe UI", 22, "bold"),
    bg="#243447",
    fg="white"
).pack(
    pady=(17, 0)
)


tk.Label(
    header,
    text="Manage students, marks and grades",
    font=("Segoe UI", 10),
    bg="#243447",
    fg="#dbe4ee"
).pack()



# DASHBOARD


dashboard = tk.Frame(
    root,
    bg="#eef2f7"
)

dashboard.pack(
    fill="x",
    padx=25,
    pady=18
)


def create_card(title, value):

    card = tk.Frame(
        dashboard,
        bg="white",
        bd=1,
        relief="solid"
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=6
    )

    tk.Label(
        card,
        text=title,
        font=("Segoe UI", 9),
        bg="white",
        fg="#64748b"
    ).pack(
        pady=(12, 2)
    )

    value_label = tk.Label(
        card,
        text=value,
        font=("Segoe UI", 20, "bold"),
        bg="white",
        fg="#243447"
    )

    value_label.pack(
        pady=(0, 12)
    )

    return value_label


total_label = create_card(
    "TOTAL STUDENTS",
    "0"
)

average_label = create_card(
    "AVERAGE",
    "0%"
)

passed_label = create_card(
    "PASSED",
    "0"
)

failed_label = create_card(
    "FAILED",
    "0"
)




# INPUT SECTION


input_frame = tk.Frame(
    root,
    bg="white",
    bd=1,
    relief="solid"
)

input_frame.pack(
    fill="x",
    padx=32,
    pady=5
)


tk.Label(
    input_frame,
    text="Student Name",
    font=("Segoe UI", 9, "bold"),
    bg="white",
    fg="#374151"
).grid(
    row=0,
    column=0,
    padx=(18, 8),
    pady=(12, 4),
    sticky="w"
)


tk.Label(
    input_frame,
    text="Roll Number",
    font=("Segoe UI", 9, "bold"),
    bg="white",
    fg="#374151"
).grid(
    row=0,
    column=1,
    padx=8,
    pady=(12, 4),
    sticky="w"
)


tk.Label(
    input_frame,
    text="Marks",
    font=("Segoe UI", 9, "bold"),
    bg="white",
    fg="#374151"
).grid(
    row=0,
    column=2,
    padx=8,
    pady=(12, 4),
    sticky="w"
)


name_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

name_entry.grid(
    row=1,
    column=0,
    padx=(18, 8),
    pady=(0, 15)
)


roll_entry = tk.Entry(
    input_frame,
    width=18,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

roll_entry.grid(
    row=1,
    column=1,
    padx=8,
    pady=(0, 15)
)


marks_entry = tk.Entry(
    input_frame,
    width=12,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

marks_entry.grid(
    row=1,
    column=2,
    padx=8,
    pady=(0, 15)
)


# BUTTONS


tk.Button(
    input_frame,
    text="SAVE STUDENT",
    command=add_student,
    font=("Segoe UI", 9, "bold"),
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    relief="flat",
    padx=14,
    pady=8,
    cursor="hand2"
).grid(
    row=1,
    column=3,
    padx=8,
    pady=(0, 15)
)


tk.Button(
    input_frame,
    text="EDIT",
    command=edit_student,
    font=("Segoe UI", 9, "bold"),
    bg="#f59e0b",
    fg="white",
    activebackground="#d97706",
    relief="flat",
    padx=18,
    pady=8,
    cursor="hand2"
).grid(
    row=1,
    column=4,
    padx=8,
    pady=(0, 15)
)


tk.Button(
    input_frame,
    text="CLEAR",
    command=clear_fields,
    font=("Segoe UI", 9, "bold"),
    bg="#64748b",
    fg="white",
    activebackground="#475569",
    relief="flat",
    padx=18,
    pady=8,
    cursor="hand2"
).grid(
    row=1,
    column=5,
    padx=8,
    pady=(0, 15)
)



# SEARCH


search_frame = tk.Frame(
    root,
    bg="#eef2f7"
)

search_frame.pack(
    fill="x",
    padx=32,
    pady=(15, 8)
)


tk.Label(
    search_frame,
    text="Search:",
    font=("Segoe UI", 10, "bold"),
    bg="#eef2f7",
    fg="#374151"
).pack(
    side="left"
)


search_entry = tk.Entry(
    search_frame,
    width=28,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

search_entry.pack(
    side="left",
    padx=10
)


tk.Button(
    search_frame,
    text="SEARCH",
    command=search_student,
    font=("Segoe UI", 9, "bold"),
    bg="#243447",
    fg="white",
    relief="flat",
    padx=15,
    pady=5,
    cursor="hand2"
).pack(
    side="left"
)


tk.Button(
    search_frame,
    text="SHOW ALL",
    command=show_all,
    font=("Segoe UI", 9, "bold"),
    bg="#e2e8f0",
    fg="#1e293b",
    relief="flat",
    padx=15,
    pady=5,
    cursor="hand2"
).pack(
    side="left",
    padx=7
)



# STUDENT TABLE


table_frame = tk.Frame(
    root,
    bg="white",
    bd=1,
    relief="solid"
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=32,
    pady=5
)


columns = (
    "Name",
    "Roll",
    "Marks",
    "Percentage",
    "Grade"
)


student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="browse"
)


student_table.heading(
    "Name",
    text="STUDENT NAME"
)

student_table.heading(
    "Roll",
    text="ROLL NUMBER"
)

student_table.heading(
    "Marks",
    text="MARKS"
)

student_table.heading(
    "Percentage",
    text="PERCENTAGE"
)

student_table.heading(
    "Grade",
    text="GRADE"
)


student_table.column(
    "Name",
    width=280
)

student_table.column(
    "Roll",
    width=160,
    anchor="center"
)

student_table.column(
    "Marks",
    width=120,
    anchor="center"
)

student_table.column(
    "Percentage",
    width=150,
    anchor="center"
)

student_table.column(
    "Grade",
    width=120,
    anchor="center"
)


# Grade colors

student_table.tag_configure(
    "excellent",
    foreground="#15803d"
)

student_table.tag_configure(
    "good",
    foreground="#2563eb"
)

student_table.tag_configure(
    "average",
    foreground="#d97706"
)

student_table.tag_configure(
    "failed",
    foreground="#dc2626"
)


scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=student_table.yview
)

student_table.configure(
    yscrollcommand=scrollbar.set
)


student_table.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


student_table.bind(
    "<Double-1>",
    select_student
)



# DELETE BUTTON


tk.Button(
    root,
    text="DELETE SELECTED STUDENT",
    command=delete_student,
    font=("Segoe UI", 9, "bold"),
    bg="#dc2626",
    fg="white",
    activebackground="#b91c1c",
    relief="flat",
    padx=20,
    pady=8,
    cursor="hand2"
).pack(
    pady=12
)



# START PROGRAM


load_data()

refresh_table()

update_dashboard()

name_entry.focus()

root.mainloop()
626",
    fg="white",
    activebackground="#b91c1c",
    relief="flat",
    padx=20,
    pady=8,
    cursor="hand2"
).pack(
    pady=12
)



# START PROGRAM


load_data()

refresh_table()

update_dashboard()

name_entry.focus()

root.mainloop()
