import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pickle
import os

# Data file path
data_file = 'event_management_data.pkl'

# Load data from the file or create an empty structure if the file doesn't exist
def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'rb') as f:
            return pickle.load(f)
    else:
        return {'employees': [], 'venues': [], 'suppliers': [], 'events': [], 'clients': [], 'guests': [], 'caterers': []}

# Save data to the file
def save_data(data):
    with open(data_file, 'wb') as f:
        pickle.dump(data, f)

# Function to add, modify, or delete data within the GUI
def modify_data(action, entity_type, entries):
    data = load_data()
    entity_id = entries['ID'].get()
    attributes = {field: entry.get() for field, entry in entries.items() if field != 'ID'}

    if action == 'add':
        data[entity_type].append({'id': entity_id, **attributes})
    elif action in ('delete', 'modify'):
        for index, entity in enumerate(data[entity_type]):
            if entity['id'] == entity_id:
                if action == 'delete':
                    data[entity_type].pop(index)
                elif action == 'modify':
                    entity.update(attributes)
                break
    save_data(data)
    messagebox.showinfo("Success", f"Data {action}ed successfully.")
    display_data()

# Display current data in the text area
def display_data():
    data = load_data()
    data_text.delete('1.0', tk.END)
    for category, items in data.items():
        data_text.insert(tk.END, f"{category.upper()}:\n")
        for item in items:
            details = ', '.join(f"{k}: {v}" for k, v in item.items())
            data_text.insert(tk.END, f"  - {details}\n")
        data_text.insert(tk.END, "\n")

# Setup the main GUI window
root = tk.Tk()
root.title("Event Management System")

# Tab control for different data categories
tab_control = ttk.Notebook(root)
categories = ['employees', 'venues', 'suppliers', 'events', 'clients', 'guests', 'caterers', 'Data View']
tabs = {category: ttk.Frame(tab_control) for category in categories[:-1]}
data_view_tab = ttk.Frame(tab_control)
tabs['Data View'] = data_view_tab
tab_control.add(data_view_tab, text='Data View')

for category, tab in tabs.items():
    tab_control.add(tab, text=category.capitalize())
    entries = {}

    if category != 'Data View':
        # Entry fields for data manipulation
        fields = {
            'employees': ['ID', 'Name', 'Department', 'Job Title', 'Basic Salary'],
            'venues': ['ID', 'Name', 'Address', 'Contact', 'Minimum Guests', 'Maximum Guests'],
            'suppliers': ['ID', 'Name', 'Address', 'Contact Details', 'Menu', 'Minimum Guests', 'Maximum Guests'],
            'events': ['ID', 'Type', 'Theme', 'Date', 'Time', 'Duration', 'Venue Address', 'Client ID', 'Guest List', 'Catering Company', 'Cleaning Company', 'Decorations Company', 'Entertainment Company', 'Furniture Supply Company', 'Invoice'],
            'clients': ['ID', 'Name', 'Address', 'Contact Details', 'Budget'],
            'guests': ['ID', 'Name', 'Address', 'Contact Details'],
            'caterers': ['ID', 'Name', 'Address', 'Contact Details', 'Menu', 'Minimum Guests', 'Maximum Guests']
        }[category]

        for field in fields:
            ttk.Label(tab, text=field).pack()
            entry = ttk.Entry(tab)
            entry.pack()
            entries[field] = entry

        # Buttons for Add, Delete, Modify
        ttk.Button(tab, text="Add", command=lambda c=category, e=entries.copy(): modify_data('add', c, e)).pack()
        ttk.Button(tab, text="Delete", command=lambda c=category, e=entries.copy(): modify_data('delete', c, e)).pack()
        ttk.Button(tab, text="Modify", command=lambda c=category, e=entries.copy(): modify_data('modify', c, e)).pack()

tab_control.pack(expand=1, fill="both")

# Text area for data view
data_text = scrolledtext.ScrolledText(data_view_tab, height=10)
data_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Button to refresh and display data
view_data_button = tk.Button(data_view_tab, text="Refresh Data", command=display_data)
view_data_button.pack(pady=10)

root.mainloop()
