import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from file_operations import save_columns_by_group
from data_analysis import calculate_statistics
from map_visualization import plot_selected_row, get_arkansas_counties_from_shapefile  # Import the Arkansas counties function
import os


df = None
script_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = os.path.join(script_dir, 'data', 'output')

original_filepath = None  # Global variable to store the path of the loaded file

# Add a global variable for the mode
mode_var = None
# Global references for buttons
load_original_button = None
convert_data_button = None
pick_converted_button = None
view_map_button = None
county_listbox_all = None
county_listbox_selected = None

def switch_mode():
    global mode_var, load_original_button, convert_data_button, pick_converted_button, view_map_button, county_listbox_all, county_listbox_selected
    mode = mode_var.get()
    if mode == 'interactive':
        # Disable all buttons in interactive mode
        load_original_button.config(state=tk.DISABLED)
        convert_data_button.config(state=tk.DISABLED)
        pick_converted_button.config(state=tk.NORMAL)
        view_map_button.config(state=tk.NORMAL)
        county_listbox_all.config(state=tk.NORMAL)  # Enable the Listbox with all counties
        county_listbox_selected.config(state=tk.NORMAL)  # Enable the Listbox for selected counties
    elif mode == 'normal':
        # Enable all buttons in normal mode
        load_original_button.config(state=tk.NORMAL)
        convert_data_button.config(state=tk.NORMAL)
        pick_converted_button.config(state=tk.NORMAL)
        view_map_button.config(state=tk.NORMAL)
        county_listbox_all.config(state=tk.DISABLED)  # Disable the Listbox for all counties in normal mode
        county_listbox_selected.config(state=tk.DISABLED)  # Disable the Listbox for selected counties in normal mode


def start_drag(event):
    index = county_listbox_all.nearest(event.y)
    county = county_listbox_all.get(index)
    county_listbox_selected.insert(tk.END, county)

def end_drag(event):
    index = county_listbox_selected.nearest(event.y)
    county = county_listbox_selected.get(index)
    county_listbox_selected.delete(index)
    county_listbox_all.insert(tk.END, county)

def load_original_data(update_dropdown, label_file_explorer):
    global df, original_filepath
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not filepath:
        return
    try:
        df = pd.read_csv(filepath)
        original_filepath = filepath  # Store the loaded file path
        update_dropdown(df.iloc[:, 0].unique())
        label_file_explorer.configure(text="Original data loaded: " + filepath)
    except Exception as e:
        label_file_explorer.configure(text="Failed to load original data: " + str(e))

def convert_original_data(label_file_explorer, original_filepath):
    global df
    if df is not None:
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            save_columns_by_group(df, output_dir, original_filepath)
            label_file_explorer.configure(text="Original data converted successfully.")
        except Exception as e:
            label_file_explorer.configure(text="Failed to convert original data: " + str(e))
    else:
        messagebox.showwarning("Warning", "No original data loaded to convert.")

def pick_converted_data(update_dropdown, label_file_explorer, row_dropdown, row_var):
    global df, original_filepath
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not filepath:
        return
    try:
        df = pd.read_csv(filepath)
        original_filepath = filepath  # Update the filepath for the converted file
        update_dropdown(df.iloc[:, 0].unique(), row_dropdown, row_var)
        label_file_explorer.configure(text="Converted data loaded: " + filepath)
    except Exception as e:
        label_file_explorer.configure(text="Failed to load converted data: " + str(e))

def view_map(county_shapefile_path, row_var):
    selected_row_name = row_var.get()
    if df is not None and selected_row_name in df['Label (Grouping)'].values:
        if original_filepath:  # Ensure filename is not None
            # Get the list of selected counties from the Listbox
            selected_counties = county_listbox_selected.get(0, tk.END)
            plot_selected_row(df, selected_row_name, county_shapefile_path, original_filepath, selected_counties)
        else:
            messagebox.showwarning("Warning", "File path is not set.")
    else:
        messagebox.showwarning("Warning", "Please select a valid row for mapping.")

def update_dropdown(options, dropdown, variable):
    dropdown['menu'].delete(0, 'end')
    for option in options:
        dropdown['menu'].add_command(label=option, command=lambda value=option: variable.set(value))

def setup_gui(county_shapefile_path, arkansas_counties):
    global mode_var, load_original_button, convert_data_button, pick_converted_button, view_map_button, county_listbox_all, county_listbox_selected
    root = tk.Tk()
    root.title("Data Processing and Visualization GUI")

    # Radio Buttons for Mode Selection
    mode_var = tk.StringVar(value='normal')  # Default mode set to 'normal'
    rb_normal = tk.Radiobutton(root, text='Normal Mode', variable=mode_var, value='normal', command=switch_mode)
    rb_interactive = tk.Radiobutton(root, text='Interactive Mode', variable=mode_var, value='interactive', command=switch_mode)
    
    rb_normal.pack(pady=5)
    rb_interactive.pack(pady=5)

    # Define buttons with global references
    load_original_button = tk.Button(root, text="Load Original Data", command=lambda: load_original_data(update_dropdown, label_file_explorer))
    convert_data_button = tk.Button(root, text="Convert Original Data", command=lambda: convert_original_data(label_file_explorer, original_filepath))
    pick_converted_button = tk.Button(root, text="Pick Converted Data", command=lambda: pick_converted_data(update_dropdown, label_file_explorer, row_dropdown, row_var))
    view_map_button = tk.Button(root, text="View Map", command=lambda: view_map(county_shapefile_path, row_var))

    # Pack buttons
    load_original_button.pack(pady=5)
    convert_data_button.pack(pady=5)
    pick_converted_button.pack(pady=5)
    view_map_button.pack(pady=5)

    label_file_explorer = tk.Label(root, text="Select a CSV file", fg="blue")
    label_file_explorer.pack(pady=10)

    row_var = tk.StringVar(root)
    row_dropdown = tk.OptionMenu(root, row_var, '')
    row_dropdown.pack(pady=5)

    # Create a Listbox for all Arkansas counties
    county_listbox_all = tk.Listbox(root, selectmode=tk.SINGLE)
    county_listbox_all.pack(pady=5)

    # Add a Scrollbar to the Listbox
    scrollbar_all = tk.Scrollbar(root, orient=tk.VERTICAL)
    county_listbox_all.config(yscrollcommand=scrollbar_all.set)
    scrollbar_all.config(command=county_listbox_all.yview)
    scrollbar_all.pack(side=tk.RIGHT, fill=tk.Y)

    # Insert Arkansas counties into the Listbox
    for county in arkansas_counties:
        county_listbox_all.insert(tk.END, county)

    # Create a Listbox for selected counties
    county_listbox_selected = tk.Listbox(root, selectmode=tk.SINGLE)
    county_listbox_selected.pack(pady=5)

    # Add a Scrollbar to the Listbox
    scrollbar_selected = tk.Scrollbar(root, orient=tk.VERTICAL)
    county_listbox_selected.config(yscrollcommand=scrollbar_selected.set)
    scrollbar_selected.config(command=county_listbox_selected.yview)
    scrollbar_selected.pack(side=tk.RIGHT, fill=tk.Y)

    # Bind drag-and-drop functionality
    county_listbox_all.bind("<Button-1>", start_drag)
    county_listbox_selected.bind("<Button-1>", start_drag)
    county_listbox_selected.bind("<ButtonRelease-1>", end_drag)

    root.mainloop()