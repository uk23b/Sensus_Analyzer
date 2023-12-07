
import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd

# Initialize a global variable to store the csv data
csv_data = None

def load_csv():
    global csv_data
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        csv_data = pd.read_csv(file_path)
        update_dropdown(csv_data['Label (Grouping)'].tolist())

def update_dropdown(options):
    dropdown['menu'].delete(0, 'end')
    for option in options:
        dropdown['menu'].add_command(label=option, command=tk._setit(selected_option, option))
    selected_option.set(options[0])

def plot_selected_row():
    if csv_data is not None:
        selected_label = selected_option.get()
        row_data = csv_data[csv_data['Label (Grouping)'] == selected_label]
        # Here we would call the map visualization function with the selected row data
        # For example: map_visualization.plot_county_data(row_data)

# Create the main window
root = tk.Tk()
root.title("CSV Viewer")

# Dropdown to select the row for mapping
selected_option = tk.StringVar(root)
dropdown = tk.OptionMenu(root, selected_option, '')
dropdown.pack()

# Button to load CSV
load_button = tk.Button(root, text="Load CSV", command=load_csv)
load_button.pack()

# Button to plot the selected row
plot_button = tk.Button(root, text="Plot Selected Row", command=plot_selected_row)
plot_button.pack()

root.mainloop()
