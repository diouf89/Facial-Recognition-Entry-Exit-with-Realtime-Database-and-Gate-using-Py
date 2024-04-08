import json
import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facemonitoringrealtime-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

ref = db.reference('Students')  # reference path of database

def load_data():
    try:
        with open('AddDatabase.txt', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open('AddDatabase.txt', 'w') as file:
        json.dump(data, file, indent=4)

def add_entry():
    new_key = entry_key.get()
    new_name = entry_name.get()
    new_section = entry_section.get()
    new_starting_year = entry_starting_year.get()
    new_total_attendance = entry_total_attendance.get()
    new_standing = entry_standing.get()
    new_year = entry_year.get()
    new_last_attendance_time = entry_last_attendance_time.get()
    new_guardian_phone_number = entry_guardian_phone_number.get()

    if new_key and new_name and new_section and new_starting_year and new_total_attendance and \
            new_standing and new_year and new_last_attendance_time and new_guardian_phone_number:
        try:
            new_starting_year = int(new_starting_year)
            new_total_attendance = int(new_total_attendance)
            new_year = int(new_year)
        except ValueError:
            messagebox.showerror('Error', 'Invalid input for numeric fields.')
            return

        data[new_key] = {
            "name": new_name,
            "section": new_section,
            "starting_year": new_starting_year,
            "total_attendance": new_total_attendance,
            "standing": new_standing,
            "year": new_year,
            "last_attendance_time": new_last_attendance_time,
            "Guardian Phone Number": new_guardian_phone_number
        }

        save_data(data)
        messagebox.showinfo('Success', 'Entry added successfully!')
        clear_input_fields()
    else:
        messagebox.showerror('Error', 'Please fill in all fields.')

def delete_entry():
    key_to_delete = entry_delete_key.get()
    if key_to_delete in data:
        del data[key_to_delete]
        save_data(data)
        messagebox.showinfo('Success', f'Entry with key {key_to_delete} deleted successfully!')
    else:
        messagebox.showerror('Error', 'Entry not found.')

def delete_all_entries():
    response = messagebox.askyesno('Delete All Entries', 'Are you sure you want to delete all entries?')
    if response:
        data.clear()
        save_data(data)
        messagebox.showinfo('Success', 'All entries deleted successfully!')

def clear_input_fields():
    entry_key.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_section.delete(0, tk.END)
    entry_starting_year.delete(0, tk.END)
    entry_total_attendance.delete(0, tk.END)
    entry_standing.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_last_attendance_time.delete(0, tk.END)
    entry_guardian_phone_number.delete(0, tk.END)
    entry_delete_key.delete(0, tk.END)

def view_entries():
    entries_window = tk.Toplevel(window)
    entries_window.title('All Entries')

    entries_text = tk.Text(entries_window)
    entries_text.insert(tk.END, json.dumps(data, indent=4))
    entries_text.pack()

def update_firebase():
    data_to_update = load_data()

    for key, value in data_to_update.items():
        ref.child(key).set(value)

    messagebox.showinfo('Success', 'Database updated successfully!')

# Load existing data from the file
data = load_data()

# Create the main window
window = tk.Tk()
window.title('Database Manager')

# Create labels
label_key = tk.Label(window, text='Key:')
label_name = tk.Label(window, text='Name:')
label_section = tk.Label(window, text='Section:')
label_starting_year = tk.Label(window, text='Starting Year:')
label_total_attendance = tk.Label(window, text='Total Attendance:')
label_standing = tk.Label(window, text='Standing:')
label_year = tk.Label(window, text='Year:')
label_last_attendance_time = tk.Label(window, text='Last Attendance Time:')
label_guardian_phone_number = tk.Label(window, text='Guardian Phone Number:')
label_delete_key = tk.Label(window, text='Key to Delete:')

# Create entry widgets
entry_key = tk.Entry(window)
entry_name = tk.Entry(window)
entry_section = tk.Entry(window)
entry_starting_year = tk.Entry(window)
entry_total_attendance = tk.Entry(window)
entry_standing = tk.Entry(window)
entry_year = tk.Entry(window)
entry_last_attendance_time = tk.Entry(window)
entry_guardian_phone_number = tk.Entry(window)
entry_delete_key = tk.Entry(window)

# Create buttons
add_button = tk.Button(window, text='Add Entry', command=add_entry)
delete_button = tk.Button(window, text='Delete Entry', command=delete_entry)
delete_all_button = tk.Button(window, text='Delete All Entries', command=delete_all_entries)
clear_button = tk.Button(window, text='Clear Input Fields', command=clear_input_fields)
view_button = tk.Button(window, text='View All Entries', command=view_entries)
update_firebase_button = tk.Button(window, text='Update Database', command=update_firebase)

# Place widgets in the window
label_key.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
label_name.grid(row=1, column=0, pady=5, padx=5, sticky=tk.W)
label_section.grid(row=2, column=0, pady=5, padx=5, sticky=tk.W)
label_starting_year.grid(row=3, column=0, pady=5, padx=5, sticky=tk.W)
label_total_attendance.grid(row=4, column=0, pady=5, padx=5, sticky=tk.W)
label_standing.grid(row=5, column=0, pady=5, padx=5, sticky=tk.W)
label_year.grid(row=6, column=0, pady=5, padx=5, sticky=tk.W)
label_last_attendance_time.grid(row=7, column=0, pady=5, padx=5, sticky=tk.W)
label_guardian_phone_number.grid(row=8, column=0, pady=5, padx=5, sticky=tk.W)
label_delete_key.grid(row=9, column=0, pady=5, padx=5, sticky=tk.W)

entry_key.grid(row=0, column=1, pady=5, padx=5)
entry_name.grid(row=1, column=1, pady=5, padx=5)
entry_section.grid(row=2, column=1, pady=5, padx=5)
entry_starting_year.grid(row=3, column=1, pady=5, padx=5)
entry_total_attendance.grid(row=4, column=1, pady=5,padx=5)
entry_standing.grid(row=5, column=1, pady=5, padx=5)
entry_year.grid(row=6, column=1, pady=5, padx=5)
entry_last_attendance_time.grid(row=7, column=1, pady=5, padx=5)
entry_guardian_phone_number.grid(row=8, column=1, pady=5, padx=5)
entry_delete_key.grid(row=9, column=1, pady=5, padx=5)

# Create buttons
add_button.grid(row=10, column=0, pady=5, padx=5)
delete_button.grid(row=10, column=1, pady=5, padx=5)
delete_all_button.grid(row=11, column=0, pady=5, padx=5)
clear_button.grid(row=11, column=1, pady=5, padx=5)
view_button.grid(row=12, column=0, columnspan=2, pady=10)
update_firebase_button.grid(row=13, column=0, columnspan=2, pady=10)

# Run the Tkinter event loop
window.mainloop()
