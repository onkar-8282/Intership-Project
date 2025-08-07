import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json, os

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
    with open(FILE, "w") as f:
        json.dump(students, f, indent=4)

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

# ------------------- Edit Student -------------------
def edit_student():
    selected = shared_tree.selection()
    if not selected:
        messagebox.showinfo("Select", "Select a student to edit.")
        return

    values = shared_tree.item(selected)["values"]
    enroll_no = values[0]

    for idx, s in enumerate(students):
        if s["enrollment_no"] == enroll_no:
            new_name = simpledialog.askstring("Edit Name", "Name:", initialvalue=s["name"])
            new_contact = simpledialog.askstring("Edit Contact", "Contact No:", initialvalue=s["contact_no"])
            new_email = simpledialog.askstring("Edit Email", "Email:", initialvalue=s["email_id"])
            new_percentage = simpledialog.askstring("Edit Percentage", "Percentage:", initialvalue=str(s["percentage"]))

            if not new_name or not new_contact or not new_email or not new_percentage:
                messagebox.showwarning("Invalid", "All fields must be filled.")
                return

            try:
                new_percentage = float(new_percentage)
            except:
                messagebox.showwarning("Invalid", "Percentage must be a number.")
                return

            students[idx] = {
                "enrollment_no": enroll_no,
                "name": new_name,
                "contact_no": new_contact,
                "email_id": new_email,
                "percentage": new_percentage
            }
            save_data()
            refresh_tree(shared_tree)
            messagebox.showinfo("Updated", "Student updated successfully.")
            return

# ------------------- Delete Student -------------------
def delete_student():
    selected = shared_tree.selection()
    if not selected:
        messagebox.showinfo("Select", "Select a student to delete.")
        return

    values = shared_tree.item(selected)["values"]
    enroll_no = values[0]

    for idx, s in enumerate(students):
        if s["enrollment_no"] == enroll_no:
            if messagebox.askyesno("Confirm", "Delete selected student?"):
                students.pop(idx)
                save_data()
                refresh_tree(shared_tree)
                messagebox.showinfo("Deleted", "Student deleted successfully.")
                return

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

    tree = ttk.Treeview(frame, columns=("Enroll", "Name", "Contact", "Email", "Perc"), show="headings", height=15)
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
tk.Button(edit_frame, text="Edit Selected Student", command=edit_student).pack(pady=10)

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
