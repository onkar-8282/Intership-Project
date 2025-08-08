import tkinter as tk
from tkinter import ttk, messagebox
import json, os, re

FILE = "students.json"

# ------------------- Data Handling -------------------
def load_data():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to load data.")
    return []

def save_data():
    try:
        with open(FILE, "w") as f:
            json.dump(students, f, indent=4)
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save data:\n{e}")

# ------------------- Refresh Treeview -------------------
def refresh_tree(treeview, data=None):
    treeview.delete(*treeview.get_children())
    for s in data if data else students:
        treeview.insert("", "end", values=(s["enrollment_no"], s["name"], s["contact_no"], s["email_id"], s["percentage"]))

# ------------------- Add Student -------------------
def add_student():
    e = enrollment_var.get().strip()
    n = name_var.get().strip()
    c = contact_var.get().strip()
    em = email_var.get().strip()
    p = percentage_var.get().strip()

    if not (e and n and c and em and p):
        messagebox.showwarning("Incomplete", "Fill all fields.")
        return

    if not re.match(r"^\d{10}$", c):
        messagebox.showwarning("Invalid", "Contact must be 10 digits.")
        return

    if not re.match(r"[^@]+@[^@]+\.[^@]+", em):
        messagebox.showwarning("Invalid", "Invalid email format.")
        return

    try:
        p = float(p)
    except ValueError:
        messagebox.showwarning("Invalid", "Percentage must be a number.")
        return

    if any(s["enrollment_no"] == e for s in students):
        messagebox.showwarning("Duplicate", "Enrollment number already exists.")
        return

    students.append({
        "enrollment_no": e,
        "name": n,
        "contact_no": c,
        "email_id": em,
        "percentage": p
    })
    save_data()
    refresh_tree(shared_tree)
    for var in [enrollment_var, name_var, contact_var, email_var, percentage_var]:
        var.set("")
    messagebox.showinfo("Success", "Student added successfully.")

# ------------------- Delete Student (Multiple Support) -------------------
def delete_student():
    selected_items = shared_tree.selection()
    if not selected_items:
        messagebox.showinfo("Select", "Select student(s) to delete.")
        return

    to_delete = []
    for item in selected_items:
        values = shared_tree.item(item)["values"]
        enroll_no = values[0]
        to_delete.append(enroll_no)

    if not messagebox.askyesno("Confirm", f"Delete {len(to_delete)} student(s)?"):
        return

    global students
    students = [s for s in students if s["enrollment_no"] not in to_delete]
    save_data()
    refresh_tree(shared_tree)
    messagebox.showinfo("Deleted", f"{len(to_delete)} student(s) deleted successfully.")

# ------------------- Search -------------------
def search(treeview, query):
    query = query.lower().strip()
    filtered = [s for s in students if query in s["enrollment_no"].lower() or query in s["name"].lower()]
    refresh_tree(treeview, filtered)

# ------------------- GUI Setup -------------------
root = tk.Tk()
root.title("Student Management System")
root.geometry("950x600")

# ------------------- Top Navigation -------------------
def show_frame(frame):
    frame.tkraise()
    refresh_tree(shared_tree)

menubar = tk.Menu(root)
root.config(menu=menubar)

frame_container = tk.Frame(root)
frame_container.pack(fill="both", expand=True)

# ------------------- Shared Treeview -------------------
def create_treeview(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree = ttk.Treeview(frame, columns=("Enroll", "Name", "Contact", "Email", "Perc"), show="headings", height=15, selectmode="extended")
    for col in ("Enroll", "Name", "Contact", "Email", "Perc"):
        tree.heading(col, text=col)
        tree.column(col, width=170, anchor="center")

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=vsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    return tree

shared_tree = create_treeview(root)

# ------------------- Add Page -------------------
add_frame = tk.Frame(frame_container)
add_frame.grid(row=0, column=0, sticky="nsew")

enrollment_var = tk.StringVar()
name_var = tk.StringVar()
contact_var = tk.StringVar()
email_var = tk.StringVar()
percentage_var = tk.StringVar()

tk.Label(add_frame, text="Add Student", font=("Arial", 16)).grid(row=0, columnspan=2, pady=10)

tk.Label(add_frame, text="Enrollment No").grid(row=1, column=0, sticky="e", padx=10, pady=5)
tk.Entry(add_frame, textvariable=enrollment_var).grid(row=1, column=1, padx=10)

tk.Label(add_frame, text="Name").grid(row=2, column=0, sticky="e", padx=10, pady=5)
tk.Entry(add_frame, textvariable=name_var).grid(row=2, column=1, padx=10)

tk.Label(add_frame, text="Contact No").grid(row=3, column=0, sticky="e", padx=10, pady=5)
tk.Entry(add_frame, textvariable=contact_var).grid(row=3, column=1, padx=10)

tk.Label(add_frame, text="Email ID").grid(row=4, column=0, sticky="e", padx=10, pady=5)
tk.Entry(add_frame, textvariable=email_var).grid(row=4, column=1, padx=10)

tk.Label(add_frame, text="Percentage").grid(row=5, column=0, sticky="e", padx=10, pady=5)
tk.Entry(add_frame, textvariable=percentage_var).grid(row=5, column=1, padx=10)

tk.Button(add_frame, text="Submit", command=add_student).grid(row=6, columnspan=2, pady=20)

# ------------------- Edit Page -------------------
edit_frame = tk.Frame(frame_container)
edit_frame.grid(row=0, column=0, sticky="nsew")

edit_search_var = tk.StringVar()
tk.Label(edit_frame, text="Edit Student", font=("Arial", 16)).pack(pady=10)
tk.Entry(edit_frame, textvariable=edit_search_var, width=40).pack()
tk.Button(edit_frame, text="Search", command=lambda: search(shared_tree, edit_search_var.get())).pack(pady=5)

edit_enrollment_var = tk.StringVar()
edit_name_var = tk.StringVar()
edit_contact_var = tk.StringVar()
edit_email_var = tk.StringVar()
edit_percentage_var = tk.StringVar()

form_frame = tk.Frame(edit_frame)
form_frame.pack(pady=10)

tk.Label(form_frame, text="Enrollment No").grid(row=0, column=0, padx=10, pady=5, sticky="e")
tk.Entry(form_frame, textvariable=edit_enrollment_var, state="disabled").grid(row=0, column=1)

tk.Label(form_frame, text="Name").grid(row=1, column=0, padx=10, pady=5, sticky="e")
tk.Entry(form_frame, textvariable=edit_name_var).grid(row=1, column=1)

tk.Label(form_frame, text="Contact No").grid(row=2, column=0, padx=10, pady=5, sticky="e")
tk.Entry(form_frame, textvariable=edit_contact_var).grid(row=2, column=1)

tk.Label(form_frame, text="Email ID").grid(row=3, column=0, padx=10, pady=5, sticky="e")
tk.Entry(form_frame, textvariable=edit_email_var).grid(row=3, column=1)

tk.Label(form_frame, text="Percentage").grid(row=4, column=0, padx=10, pady=5, sticky="e")
tk.Entry(form_frame, textvariable=edit_percentage_var).grid(row=4, column=1)

def on_row_select(event):
    selected = shared_tree.selection()
    if not selected:
        return
    values = shared_tree.item(selected[0])["values"]
    edit_enrollment_var.set(values[0])
    edit_name_var.set(values[1])
    edit_contact_var.set(values[2])
    edit_email_var.set(values[3])
    edit_percentage_var.set(values[4])

def update_student():
    enroll = edit_enrollment_var.get()
    name = edit_name_var.get().strip()
    contact = edit_contact_var.get().strip()
    email = edit_email_var.get().strip()
    perc = edit_percentage_var.get().strip()

    if not (name and contact and email and perc):
        messagebox.showwarning("Incomplete", "All fields must be filled.")
        return

    try:
        perc = float(perc)
    except ValueError:
        messagebox.showwarning("Invalid", "Percentage must be a number.")
        return

    for idx, s in enumerate(students):
        if s["enrollment_no"] == enroll:
            students[idx]["name"] = name
            students[idx]["contact_no"] = contact
            students[idx]["email_id"] = email
            students[idx]["percentage"] = perc
            save_data()
            refresh_tree(shared_tree)
            messagebox.showinfo("Updated", "Student updated successfully.")
            return

tk.Button(edit_frame, text="Update Student", command=update_student).pack(pady=10)
tk.Button(edit_frame, text="Clear Fields", command=lambda: [v.set("") for v in [edit_enrollment_var, edit_name_var, edit_contact_var, edit_email_var, edit_percentage_var]]).pack()

shared_tree.bind("<<TreeviewSelect>>", on_row_select)

# ------------------- Delete Page -------------------
delete_frame = tk.Frame(frame_container)
delete_frame.grid(row=0, column=0, sticky="nsew")

delete_search_var = tk.StringVar()
tk.Label(delete_frame, text="Delete Student", font=("Arial", 16)).pack(pady=10)
tk.Entry(delete_frame, textvariable=delete_search_var, width=40).pack()
tk.Button(delete_frame, text="Search", command=lambda: search(shared_tree, delete_search_var.get())).pack(pady=5)
tk.Button(delete_frame, text="Delete Selected Student", command=delete_student).pack(pady=10)

# ------------------- Navigation Menu -------------------
menubar.add_command(label="Add Student", command=lambda: show_frame(add_frame))
menubar.add_command(label="Edit Student", command=lambda: show_frame(edit_frame))
menubar.add_command(label="Delete Student", command=lambda: show_frame(delete_frame))

# ------------------- Load and Start -------------------
students = load_data()
show_frame(add_frame)
root.mainloop()
