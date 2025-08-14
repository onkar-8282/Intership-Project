import tkinter as tk
from tkinter import ttk, messagebox
import json, os

# ------------------- File Paths -------------------
USERS_FILE = "users.json"
STUDENTS_FILE = "students.json"

# ------------------- Data Handling -------------------
def load_json(file):
    if os.path.exists(file):
        try:
            with open(file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ------------------- Student CRUD -------------------
def refresh_tree(data_list=None):
    for row in tree_search.get_children():
        tree_search.delete(row)
    data_list = data_list if data_list is not None else students
    for student in data_list:
        tree_search.insert("", "end", values=(student["enrollment_no"], student["name"], student["contact_no"],
                                              student["email_id"], student["percentage"]))

def add_student():
    if not enroll_var.get() or not name_var.get() or not contact_var.get() or not email_var.get() or not percent_var.get():
        messagebox.showerror("Error", "All fields are required.")
        return
    if not percent_var.get().replace('.', '', 1).isdigit():
        messagebox.showerror("Error", "Percentage must be a number.")
        return
    students.append({
        "enrollment_no": enroll_var.get(),
        "name": name_var.get(),
        "contact_no": contact_var.get(),
        "email_id": email_var.get(),
        "percentage": float(percent_var.get())
    })
    save_json(STUDENTS_FILE, students)
    refresh_tree()
    messagebox.showinfo("Success", "Student added successfully.")
    enroll_var.set(""); name_var.set(""); contact_var.set(""); email_var.set(""); percent_var.set("")

def search_student():
    term = search_var.get().lower()
    filtered = [s for s in students if term in s["name"].lower() or term in s["enrollment_no"].lower()]
    refresh_tree(filtered)

def load_edit_students():
    edit_tree.delete(*edit_tree.get_children())
    for student in students:
        edit_tree.insert("", "end",
                         values=(student["enrollment_no"], student["name"], student["contact_no"], student["email_id"],
                                 student["percentage"]))

def edit_selected():
    selected = edit_tree.selection()
    if not selected:
        messagebox.showerror("Error", "No student selected.")
        return
    index = edit_tree.index(selected)
    student = students[index]
    enroll_edit.set(student["enrollment_no"])
    name_edit.set(student["name"])
    contact_edit.set(student["contact_no"])
    email_edit.set(student["email_id"])
    percent_edit.set(student["percentage"])

def save_edit():
    selected = edit_tree.selection()
    if not selected:
        return
    index = edit_tree.index(selected)
    students[index] = {
        "enrollment_no": enroll_edit.get(),
        "name": name_edit.get(),
        "contact_no": contact_edit.get(),
        "email_id": email_edit.get(),
        "percentage": float(percent_edit.get())
    }
    save_json(STUDENTS_FILE, students)
    load_edit_students()
    messagebox.showinfo("Success", "Student updated successfully.")

def load_delete_students():
    delete_tree.delete(*delete_tree.get_children())
    for student in students:
        delete_tree.insert("", "end", values=(student["enrollment_no"], student["name"], student["contact_no"],
                                              student["email_id"], student["percentage"]))

def delete_selected():
    selected = delete_tree.selection()
    if not selected:
        messagebox.showerror("Error", "No student selected.")
        return
    index = delete_tree.index(selected)
    del students[index]
    save_json(STUDENTS_FILE, students)
    load_delete_students()
    refresh_tree()
    messagebox.showinfo("Deleted", "Student record deleted successfully.")

# ------------------- Login Handling -------------------
def check_login():
    username = username_var.get().strip()
    password = password_var.get().strip()

    for user in users:
        if user["username"] == username and user["password"] == password:
            login_frame.pack_forget()
            open_main_app()
            return
    messagebox.showerror("Login Failed", "Invalid username or password.")

# ------------------- Sign-Up Handling -------------------
def go_to_signup():
    login_frame.pack_forget()
    signup_frame.pack(fill="both", expand=True)

def go_to_login():
    signup_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

def create_account():
    new_username = signup_username_var.get().strip()
    new_password = signup_password_var.get().strip()
    if not new_username or not new_password:
        messagebox.showerror("Error", "All fields are required.")
        return
    for user in users:
        if user["username"] == new_username:
            messagebox.showerror("Error", "Username already exists.")
            return
    users.append({"username": new_username, "password": new_password})
    save_json(USERS_FILE, users)
    messagebox.showinfo("Success", "Account created successfully.")
    go_to_login()

# ------------------- Main App -------------------
def open_main_app():
    main_frame.pack(fill="both", expand=True)
    refresh_tree()
    load_edit_students()
    load_delete_students()

    menubar = tk.Menu(root)
    root.config(menu=menubar)
    student_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Student", menu=student_menu)
    student_menu.add_command(label="Add Student", command=lambda: notebook.select(tab_add))
    student_menu.add_command(label="Search Student", command=lambda: notebook.select(tab_search))
    student_menu.add_command(label="Edit Student", command=lambda: notebook.select(tab_edit))
    student_menu.add_command(label="Delete Student", command=lambda: notebook.select(tab_delete))
    student_menu.add_separator()
    student_menu.add_command(label="Exit", command=root.quit)

# ------------------- Tkinter UI -------------------
root = tk.Tk()
root.title("Student Management System with Login")
root.geometry("900x600")

users = load_json(USERS_FILE)
students = load_json(STUDENTS_FILE)

# ------------------- Login Frame -------------------
login_frame = tk.Frame(root)
login_frame.pack(fill="both", expand=True)

tk.Label(login_frame, text="Login", font=("Arial", 16)).pack(pady=10)

username_var = tk.StringVar()
password_var = tk.StringVar()

tk.Label(login_frame, text="Username").pack()
tk.Entry(login_frame, textvariable=username_var).pack(pady=5)
tk.Label(login_frame, text="Password").pack()
tk.Entry(login_frame, textvariable=password_var, show="*").pack(pady=5)

tk.Button(login_frame, text="Login", command=check_login).pack(pady=10)
tk.Button(login_frame, text="Create Account", command=go_to_signup).pack()

# ------------------- Signup Frame -------------------
signup_frame = tk.Frame(root)

tk.Label(signup_frame, text="Create Account", font=("Arial", 16)).pack(pady=10)

signup_username_var = tk.StringVar()
signup_password_var = tk.StringVar()

tk.Label(signup_frame, text="Username").pack()
tk.Entry(signup_frame, textvariable=signup_username_var).pack(pady=5)
tk.Label(signup_frame, text="Password").pack()
tk.Entry(signup_frame, textvariable=signup_password_var, show="*").pack(pady=5)

tk.Button(signup_frame, text="Sign Up", command=create_account).pack(pady=10)
tk.Button(signup_frame, text="Back to Login", command=go_to_login).pack()

# ------------------- Main App Frame -------------------
main_frame = tk.Frame(root)

notebook = ttk.Notebook(main_frame)
notebook.pack(fill="both", expand=True)

# --- Add Student Tab ---
tab_add = tk.Frame(notebook)
notebook.add(tab_add, text="Add Student")

enroll_var = tk.StringVar()
name_var = tk.StringVar()
contact_var = tk.StringVar()
email_var = tk.StringVar()
percent_var = tk.StringVar()

labels = ["Enrollment No", "Name", "Contact No", "Email ID", "Percentage"]
vars = [enroll_var, name_var, contact_var, email_var, percent_var]

for i, (lbl, var) in enumerate(zip(labels, vars)):
    tk.Label(tab_add, text=lbl).grid(row=i, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(tab_add, textvariable=var).grid(row=i, column=1, pady=5)

tk.Button(tab_add, text="Add Student", command=add_student).grid(row=5, column=0, columnspan=2, pady=10)

# --- Search Student Tab ---
tab_search = tk.Frame(notebook)
notebook.add(tab_search, text="Search Student")

search_var = tk.StringVar()
tk.Entry(tab_search, textvariable=search_var).pack(pady=5)
tk.Button(tab_search, text="Search", command=search_student).pack(pady=5)

columns = ("enroll", "name", "contact", "email", "percent")
tree_search = ttk.Treeview(tab_search, columns=columns, show="headings")
for col in columns:
    tree_search.heading(col, text=col.capitalize())
tree_search.pack(fill="both", expand=True)

# --- Edit Student Tab ---
tab_edit = tk.Frame(notebook)
notebook.add(tab_edit, text="Edit Student")

edit_tree = ttk.Treeview(tab_edit, columns=columns, show="headings")
for col in columns:
    edit_tree.heading(col, text=col.capitalize())
edit_tree.pack(fill="both", expand=True)

edit_form = tk.Frame(tab_edit)
edit_form.pack(pady=10)

enroll_edit = tk.StringVar()
name_edit = tk.StringVar()
contact_edit = tk.StringVar()
email_edit = tk.StringVar()
percent_edit = tk.StringVar()

for i, (lbl, var) in enumerate(zip(labels, [enroll_edit, name_edit, contact_edit, email_edit, percent_edit])):
    tk.Label(edit_form, text=lbl).grid(row=i, column=0)
    tk.Entry(edit_form, textvariable=var).grid(row=i, column=1)

tk.Button(edit_form, text="Load Selected", command=edit_selected).grid(row=5, column=0, pady=5)
tk.Button(edit_form, text="Save Changes", command=save_edit).grid(row=5, column=1, pady=5)

# --- Delete Student Tab ---
tab_delete = tk.Frame(notebook)
notebook.add(tab_delete, text="Delete Student")

delete_tree = ttk.Treeview(tab_delete, columns=columns, show="headings")
for col in columns:
    delete_tree.heading(col, text=col.capitalize())
delete_tree.pack(fill="both", expand=True)
tk.Button(tab_delete, text="Delete Selected", command=delete_selected).pack(pady=5)

root.mainloop()
