import tkinter as tk
from tkinter import filedialog
import pandas as pd

# Function to load a CSV file and update the label with the file path
def load_file():
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        try:
            df = pd.read_csv(filepath)
            label_file_explorer.configure(text="File Opened: " + filepath)
            # Now you can use df as needed, for example:
            # row_values = get_row_values_by_name(df, 'Your Row Name')
            # print(row_values)
        except Exception as e:
            label_file_explorer.configure(text="Failed to open file: " + str(e))

# Function to retrieve values by row name from the DataFrame
def get_row_values_by_name(df, row_name):
    """
    Retrieves the values of a specified row from a DataFrame based on the row name,
    using the first column as the identifier.

    Parameters:
    df (pandas.DataFrame): The DataFrame to search.
    row_name (str): The name of the row to retrieve.

    Returns:
    pandas.Series or None: The values of the row if found, otherwise None.
    """
    if df.empty:
        print("DataFrame is empty.")
        return None

    # Find the row by the identifier in the first column
    row_data = df[df.iloc[:, 0] == row_name]
    if row_data.empty:
        print(f"Row named '{row_name}' not found.")
        return None

    # Return the values of the first row if multiple rows have the same name
    return row_data.iloc[0].values[1:]  # Skip the first column which is the identifier

# Create the main window
root = tk.Tk()
root.title('CSV File Loader')

# Set window size
root.geometry("600x400")

# Create a label to show the file path
label_file_explorer = tk.Label(root, text="Select a CSV file", width=100, height=4, fg="blue")
label_file_explorer.pack()

# Create a button to load the file
button_load_file = tk.Button(root, text="Load File", command=load_file)
button_load_file.pack()

# Run the GUI main loop
root.mainloop()
