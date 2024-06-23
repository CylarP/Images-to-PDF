import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import img2pdf
import os
import subprocess
import sys

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 700
SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg')
IMAGE_SIZE = (150, 150)

def load_image(path, size=IMAGE_SIZE):
    try:
        img = Image.open(path)
        img.thumbnail(size)
        photo = ImageTk.PhotoImage(img)
        return photo, img.size
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None, (0, 0)

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        if any(f.lower().endswith(SUPPORTED_EXTENSIONS) for f in os.listdir(folder_path)):
            folder_path_var.set(folder_path)
            show_png_files(folder_path)
        else:
            messagebox.showwarning("Warning", "No supported image files found in the selected folder.")

def show_png_files(dirname):
    tree.delete(*tree.get_children())
    max_height = 0
    for idx, fname in enumerate(sorted(os.listdir(dirname)), start=1):
        if fname.lower().endswith(SUPPORTED_EXTENSIONS):
            full_path = os.path.join(dirname, fname)
            img, (width, height) = load_image(full_path)
            if img:
                item = tree.insert('', 'end', text='', image=img, values=(idx, fname), tags=(full_path,))
                tree.image_references[full_path] = img
                max_height = max(max_height, height)
    
    style = ttk.Style()
    style.configure("Treeview", rowheight=max_height + 10)
    update_numbers()

def update_numbers():
    for idx, item in enumerate(tree.get_children(), start=1):
        tree.set(item, 'Number', idx)

def move_up():
    selected = tree.selection()
    for item in selected:
        idx = tree.index(item)
        if idx > 0:
            tree.move(item, tree.parent(item), idx-1)
    update_numbers()

def move_down():
    selected = tree.selection()
    for item in reversed(selected):
        idx = tree.index(item)
        if idx < len(tree.get_children()) - 1:
            tree.move(item, tree.parent(item), idx+1)
    update_numbers()

def remove_file():
    selected = tree.selection()
    for item in selected:
        del tree.image_references[tree.item(item)['tags'][0]]
        tree.delete(item)
    update_numbers()

def convert():
    imgs = [tree.item(child)['tags'][0] for child in tree.get_children()]
    if not imgs:
        messagebox.showinfo("Info", "Add Images to convert.")
        return
    try:
        with open("result.pdf", "wb") as f:
            f.write(img2pdf.convert(imgs))
        messagebox.showinfo("Info", "Successfully converted!")
        subprocess.Popen(f'explorer "{os.getcwd()}"')
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

window = tk.Tk()
window.title("IMG2PDF")
window.iconbitmap(sys.executable)

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

position_top = int(screen_height / 2 - WINDOW_HEIGHT / 2)
position_right = int(screen_width / 2 - WINDOW_WIDTH / 2)

window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{position_right}+{position_top}")

folder_path_var = tk.StringVar()

label = tk.Label(window, text="이미지 파일이 포함된 폴더 선택 : ")
label.grid(row=0, column=0, sticky="w")

folder_entry = tk.Entry(window, textvariable=folder_path_var, width=50)
folder_entry.grid(row=1, column=0, padx=5, pady=5)

browse_button = tk.Button(window, text="Browse", command=browse_folder)
browse_button.grid(row=1, column=1, padx=5, pady=5)

png_files_label = tk.Label(window, text="이미지 파일 목록 (png, jpg):")
png_files_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

tree = ttk.Treeview(window, columns=('Number', 'Filename'), show='tree headings', selectmode='extended', height=10)
tree.heading('#0', text='Image')
tree.heading('Number', text='No.')
tree.heading('Filename', text='Filename')
tree.column('#0', width=IMAGE_SIZE[0] + 10, stretch=False)
tree.column('Number', width=50, anchor='center')
tree.column('Filename', width=300)
tree.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
scrollbar.grid(row=3, column=2, sticky="ns")
tree.configure(yscrollcommand=scrollbar.set)

tree.image_references = {}

button_frame = tk.Frame(window)
button_frame.grid(row=4, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

up_button = tk.Button(button_frame, text="Up", command=move_up, width=6)
up_button.pack(side="left", padx=2)

down_button = tk.Button(button_frame, text="Down", command=move_down, width=6)
down_button.pack(side="left", padx=2)

remove_button = tk.Button(button_frame, text="Remove", command=remove_file, width=6)
remove_button.pack(side="left", padx=2)

convert_button = tk.Button(button_frame, text="Convert", command=convert, width=6)
convert_button.pack(side="right", padx=2)

style = ttk.Style()
style.configure("Treeview", rowheight=IMAGE_SIZE[1] + 10)

window.columnconfigure(0, weight=1)
window.rowconfigure(3, weight=1)

window.mainloop()

# pyinstaller --onefile --noconsole --icon=icon.ico converter.py
