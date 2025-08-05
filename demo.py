import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json, os

FILE = "students.json"

# Load data with error handling
def load_data():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to load student data. File may be corrupted.")
            return []
    return []

# Save data with pretty formatting
def save_data():
    with open(FILE, "w") as f:
        json.dump(students, f, indent=4)

# Add student
def add_student():
    enrollment_no = enrollment_var.get().strip()
    name = name_var.get().strip()
    percentage = percentage_var.get().strip()

    try:
        perc = float(percentage)
    except ValueError:
        messagebox.showwarning("Invalid", "Percentage must be a number.")
        return

    if enrollment_no and name:
        if any(s["enrollment_no"] == enrollment_no for s in students):
            messagebox.showwarning("Duplicate", "Enrollment number already exists.")
            return
        students.append({"enrollment_no": enrollment_no, "name": name, "percentage": perc})
        save_data()
        refresh_table()
        enrollment_var.set("")
        name_var.set("")
        percentage_var.set("")
    else:
        messagebox.showwarning("Invalid", "Fill all fields correctly.")

# Edit selected student
def edit_student():
    selected = tree.selection()
    if selected:
        idx = tree.index(selected)
        s = students[idx]

        new_enrollment = simpledialog.askstring("Edit Enrollment", "Enrollment:", initialvalue=str(s["enrollment_no"]))
        new_name = simpledialog.askstring("Edit Name", "Name:", initialvalue=s["name"])
        new_percentage = simpledialog.askstring("Edit Percentage", "Percentage:", initialvalue=str(s["percentage"]))

        try:
            perc = float(new_percentage)
        except:
            messagebox.showwarning("Invalid", "Percentage must be a number.")
            return

        try:
            enroll = int(new_enrollment)
        except:
            messagebox.showwarning("Invalid", "Enrollment must be a number.")
            return

        if new_name:
            students[idx]["name"] = new_name
            students[idx]["percentage"] = new_percentage
            students[idx]["enrollment"] = new_enrollment
            save_data()
            refresh_table()

# Delete student with confirmation
def delete_student():
    selected = tree.selection()
    if selected:
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?"):
            idx = tree.index(selected)
            students.pop(idx)
            save_data()
            refresh_table()

# Refresh table
def refresh_table(filtered=None):
    tree.delete(*tree.get_children())
    data = filtered if filtered is not None else students
    for s in data:
        tree.insert("", tk.END, values=(s["enrollment_no"], s["name"], s["percentage"]))

# Search filter
def search_student():
    query = search_var.get().lower().strip()
    filtered = [s for s in students if query in s["enrollment_no"].lower() or query in s["name"].lower()]
    refresh_table(filtered)

# Clear search
def clear_search():
    search_var.set("")
    refresh_table()

# GUI setup
root = tk.Tk()
root.title("Student Management")
root.geometry("520x580")
root.resizable(False, False)

# Form frame
form = tk.Frame(root)
form.pack(pady=10)

enrollment_var = tk.StringVar()
name_var = tk.StringVar()
percentage_var = tk.StringVar()

tk.Label(form, text="Enrollment No:").grid(row=0, column=0, sticky="e")
tk.Entry(form, textvariable=enrollment_var).grid(row=0, column=1)

tk.Label(form, text="Name:").grid(row=1, column=0, sticky="e")
tk.Entry(form, textvariable=name_var).grid(row=1, column=1)

tk.Label(form, text="Percentage:").grid(row=2, column=0, sticky="e")
tk.Entry(form, textvariable=percentage_var).grid(row=2, column=1)

tk.Button(form, text="Add Student", command=add_student, bg="blue", fg="white").grid(row=3, columnspan=2, pady=5)

# Search frame
search_frame = tk.Frame(root)
search_frame.pack(pady=5)

search_var = tk.StringVar()
tk.Entry(search_frame, textvariable=search_var, width=30).grid(row=0, column=0, padx=5)
tk.Button(search_frame, text="🔍", command=search_student).grid(row=0, column=1, padx=5)
tk.Button(search_frame, text="❌", command=clear_search).grid(row=0, column=2)

# Table Frame
table_frame = tk.Frame(root)
table_frame.pack(pady=10, fill=tk.BOTH, expand=True)

tree = ttk.Treeview(table_frame, columns=("Enrollment", "Name", "Percentage"), show="headings")
tree.heading("Enrollment", text="Enrollment No")
tree.heading("Name", text="Name")
tree.heading("Percentage", text="Percentage")

tree.column("Enrollment", width=150)
tree.column("Name", width=150)
tree.column("Percentage", width=150)

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar only for Treeview
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Button Frame
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Edit", width=15, command=edit_student, bg="green", fg="white").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Delete", width=15, command=delete_student, bg="red", fg="white").grid(row=0, column=1, padx=5)

# Load and show data
students = load_data()
refresh_table()

root.mainloop()
