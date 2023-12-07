import tkinter as tk
from tkinter import filedialog

def load_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        print(f"File selected: {filepath}")
        # You can add code here to handle the file

def setup_gui():
    # Create the main window
    root = tk.Tk()
    root.title("File Loader GUI")
    root.geometry("800x600")

    # Create a 'Load File' button
    load_button = tk.Button(root, text="Load File", command=load_file)
    load_button.pack(pady=20)

    # Start the GUI event loop
    root.mainloop()

if __name__ == '__main__':
    setup_gui()
