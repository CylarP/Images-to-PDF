import tkinter as tk
from tkinter import filedialog
import img2pdf
import os
import subprocess
import sys

def browse_folder():
	folder_path = filedialog.askdirectory()
	if folder_path:
		folder_path_var.set(folder_path)
		show_png_files(folder_path)

def show_png_files(dirname):
	png_files = []
	for fname in os.listdir(dirname):
		if fname.endswith(".png") or fname.endswith(".jpg"):
			png_files.append(os.path.join(dirname, fname))
	png_files_listbox.delete(0, tk.END)
	for file in png_files:
		png_files_listbox.insert(tk.END, file)

def Convert():
	imgs = png_files_listbox.get(0, tk.END)
	with open("result.pdf","wb") as f:
		f.write(img2pdf.convert(imgs))
	tk.messagebox.showinfo("Info", "Successfully converted!")
	subprocess.Popen(f'explorer "{os.getcwd()}"')

def show_message():
	tk.messagebox.showinfo("Info", "Add Images to convert.")

def move_up():
    selected = png_files_listbox.curselection()
    if selected and selected[0] > 0:
        index = selected[0]
        value = png_files_listbox.get(index)
        png_files_listbox.delete(index)
        png_files_listbox.insert(index-1, value)
        png_files_listbox.selection_set(index-1)
   
def move_down():
	selected = png_files_listbox.curselection()
	if selected and selected[0] < png_files_listbox.size()-1:
		index = selected[0]
		value = png_files_listbox.get(index)
		png_files_listbox.delete(index)
		png_files_listbox.insert(index+1, value)
		png_files_listbox.selection_set(index+1)

def remove_file():
	selected_index = png_files_listbox.curselection()
	if selected_index:
		png_files_listbox.delete(selected_index)

window = tk.Tk()
window.title("IMG2PDF")
window.iconbitmap(sys.executable)

window_width = 360
window_height = 300

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

#input
folder_path_var = tk.StringVar()

label = tk.Label(window, text="이미지 파일이 포함된 폴더선택 : ")
label.grid(row=0, column=0, sticky="w")

folder_entry = tk.Entry(window, textvariable=folder_path_var, width=40)
folder_entry.grid(row=1, column=0)

browse_button = tk.Button(window, text="Browse", command=browse_folder)
browse_button.grid(row=1, column=2)

# PNG files
png_files_label = tk.Label(window, text="이미지 파일 목록(png, jpg):")
png_files_label.grid(row=2, column=0, sticky="w")

png_files_listbox = tk.Listbox(window, height=10, width=40, selectmode='SINGLE')
png_files_listbox.grid(row=3, column=0, sticky="w")

scrollbar_frame = tk.Frame(window, height=40)
scrollbar_frame.grid(row=3, column=1, sticky="ns")

# Create the scrollbar
scrollbar = tk.Scrollbar(scrollbar_frame, orient="vertical")
scrollbar.config(command=png_files_listbox.yview)
scrollbar.pack(side="left", fill="both")

# Attach the scrollbar to the listbox
png_files_listbox.config(yscrollcommand=scrollbar.set)

button_frame = tk.Frame(window)
button_frame.grid(row=3, column=2, sticky="nw")

up_button = tk.Button(button_frame, text="Up", command=move_up, width=6)
up_button.pack(side="top")

down_button = tk.Button(button_frame, text="Down", command=move_down, width=6)
down_button.pack(side="top")

empty_row_frame = tk.Label(button_frame, text="")
empty_row_frame.pack(side="top")

remove_button = tk.Button(button_frame, text="Remove", command=remove_file, width=6)
remove_button.pack(side="top")

# Convert button
empty_row = tk.Label(window, text="")
empty_row.grid(row=4, column=0)

convert_button = tk.Button(window, text="Convert", command=lambda: show_message() if png_files_listbox.size() == 0 else Convert())
convert_button.grid(row=5, column=2)

window.mainloop()

# pyinstaller --onefile --noconsole --icon=icon.ico converter.py