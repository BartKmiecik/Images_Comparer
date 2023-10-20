from tkinter import *
from tkinter import ttk, filedialog
import os
from PIL import Image, ImageTk
import pyautogui
from pathlib import Path
import re

mode = False
offsetY, offsetX = 0, 0
screen_width, screen_height = pyautogui.size()
width, height = 960, 540
references_images_directory = filedialog.askdirectory(title="Select Reference Folder")
renders_images_directory = filedialog.askdirectory(title="Select Renders Folder")
folder_one = Path(references_images_directory)
folder_two = Path(renders_images_directory)

def _p_file_sort_key(file_path):
    return int(re.match(r"(\d+)", file_path.name[-6:].replace('_', '0')).group(1))

types = ('*.png', '*.jpg')
path_list = []
carpaint_types = ('*')
first_list, second_list = [], []

third_list = folder_two.glob(carpaint_types)
for s in third_list:
    second_list.append(os.path.basename(s))


for carpaint in folder_one.glob(carpaint_types):
    if os.path.basename(carpaint) in second_list:
        path_list.append(os.path.basename(carpaint))


first_list, second_list = [], []

for path in path_list:
    for typed in types:
        f1 = sorted(folder_one.glob(path + "/" + typed), key=_p_file_sort_key)
        if len(f1) > 0:
            first_list.extend(f1)
        f2 = sorted(folder_two.glob(path + "/" + typed), key=_p_file_sort_key)
        if len(f2) > 0:
            second_list.extend(f2)


counter_first = 0
counter_second = 36
img, img2, img3, img4 = None, None, None, None

def Update_Panels():
    global counter_first, counter_second, mode
    global img, img2, img3, img4
    img = Image.open(first_list[counter_first]).convert('RGB')
    if mode:
        img = img.crop((0 + offsetX, offsetY, width + offsetX, height + offsetY))
    img = img.resize((width, height))
    stgImg = ImageTk.PhotoImage(img)
    label1.configure(image=stgImg)
    label1.image = stgImg
    img2 = Image.open(second_list[counter_first]).convert('RGB')
    if mode:
        img2 = img2.crop((width + offsetX, offsetY, width * 2 + offsetX, height + offsetY))
    img2 = img2.resize((width, height))
    stgImg2 = ImageTk.PhotoImage(img2)
    label2.configure(image=stgImg2)
    label2.image = stgImg2
    img3 = Image.open(first_list[counter_second]).convert('RGB')
    if mode:
        img3 = img3.crop((0 + offsetX, height + offsetY, width + offsetX, height * 2 + offsetY))
    img3 = img3.resize((width, height))
    stgImg3 = ImageTk.PhotoImage(img3)
    label3.configure(image=stgImg3)
    label3.image = stgImg3
    img4 = Image.open(second_list[counter_second]).convert('RGB')
    if mode:
        img4 = img4.crop((width + offsetX, height + offsetY, width * 2 + offsetX, height * 2 + offsetY))
    img4 = img4.resize((width, height))
    stgImg4 = ImageTk.PhotoImage(img4)
    label4.configure(image=stgImg4)
    label4.image = stgImg4

def Both_Left():
    global counter_first, counter_second, mode
    counter_first += 1
    counter_second += 1
    if counter_first > len(first_list)-1: counter_first = 0
    if counter_second > len(first_list)-1: counter_second = 0
    Update_Panels()

def chang_offsets():
    global offsetY, offsetX
    x, y = pyautogui.position()
    offsetY = -int(y - height)
    offsetX = -int(x - width)
    Update_Panels()

def Both_Right():
    global counter_first, counter_second, img, img2, img3, img4, mode
    counter_first -= 1
    if counter_first < 0: counter_first = len(first_list)-1
    counter_second -= 1
    if counter_second < 0: counter_second = len(first_list) - 1
    Update_Panels()

def key_released(e):
    # print(e.keycode)
    global counter_first, mode, offsetY
    if e.keycode == 32:
        mode = not mode
        Update_Panels()
    if e.keycode == 37:
        Both_Left()
    if e.keycode == 38:
        offsetY += 50
    if e.keycode == 39:
        Both_Right()
    if e.keycode == 40:
        offsetY -= 50

def key_update(e):
    if e.keycode == 17:
        chang_offsets()

root = Tk()
root.configure(bg='#BAC1F5',bd=0, highlightthickness=0)
frame = Frame(root, bg='black',highlightthickness=0)
frame.configure(bd=0, highlightthickness=0)
root.resizable(True, False)
root.state('zoomed')

img = Image.open(first_list[counter_first]).convert('RGB')
img = img.resize((width, height))
stgImg = ImageTk.PhotoImage(img)
label1 = ttk.Label(root, image=stgImg)
label1.grid(column=0, row=0,sticky="news")
img2 = Image.open(second_list[counter_first]).convert('RGB')
img2 = img2.resize((width, height))
stgImg2 = ImageTk.PhotoImage(img2)
label2 = ttk.Label(root, image=stgImg2)
label2.grid(column=1, row=0,sticky="news")
img3 = Image.open(first_list[counter_second]).convert('RGB')
img3 = img3.resize((width, height))
stgImg3 = ImageTk.PhotoImage(img3)
label3 = ttk.Label(root, image=stgImg3)
label3.grid(column=0, row=1,sticky="news")
img4 = Image.open(second_list[counter_second]).convert('RGB')
img4 = img4.resize((width, height))
stgImg4 = ImageTk.PhotoImage(img4)
label4 = ttk.Label(root, image=stgImg4)
label4.grid(column=1, row=1,sticky="news")

root.bind('<KeyRelease>',key_released )
root.bind('<KeyPress>', key_update)
root.mainloop()