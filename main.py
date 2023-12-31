from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfilename
import os
from pathlib import Path
from PIL import Image, ImageTk
import pyautogui
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import re

screen_width, screen_height = pyautogui.size()
width, height = 960, 540
references_images_directory = filedialog.askdirectory(title="Select Reference Folder")
renders_images_directory = filedialog.askdirectory(title="Select Renders Folder")
folder_one = Path(references_images_directory)
folder_two = Path(renders_images_directory)

# folder_one = Path('ToExclude/NBV_Org')
# folder_two = Path("ToExclude/NBV_Rend")

def _p_file_sort_key(file_path):
    return int(re.match(r"(\d+)", file_path.name[-6:].replace('_', '0')).group(1))

types = ("*.png", "*.jpg")
first_list, second_list = [], []
for typed in types:
    f1 = sorted(folder_one.glob(typed), key=_p_file_sort_key)
    if len(f1) > 0:
        first_list.extend(f1)
    f2 = sorted(folder_two.glob(typed), key=_p_file_sort_key)
    if len(f2) > 0:
        second_list.extend(f2)

# first_list = sorted(folder_one.glob("*.png"), key=_p_file_sort_key)
# second_list = sorted(folder_two.glob("*.jpg"), key=_p_file_sort_key)


counter_first = 0
counter_second = 0
img, img2 = None, None

def error(img1, img2):
   # img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
   # img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
   diff = cv2.subtract(img1, img2)
   # diff = img1 - img2
   err = np.sum(diff**2)
   mse = err/(float(height*width))
   # msre = np.sqrt(mse)
   return mse, diff

def show_diff():
    global img, img2
    match_error12, diff12 = error(np.asarray(img), np.asarray(img2))
    # diff_img_shaped = np.reshape(diff12, (width, height))
    diff_img = Image.fromarray(diff12)
    stgImg3 = ImageTk.PhotoImage(diff_img)
    label3 = ttk.Label(root, image=stgImg3)
    label3.grid(column=0, row=4, sticky="news")
    label3.configure(image=stgImg3)
    label3.image = stgImg3
    match_error_label = ttk.Label(text=str(match_error12))
    match_error_label.grid(column=0, row=2, sticky="news")
    match_error_label.configure()

def Left_Window():
    global counter_first
    global img
    counter_first += 1
    if counter_first > len(first_list)-1: counter_first = 0
    img = Image.open(first_list[counter_first]).convert('RGB')
    img = img.resize((width, height))
    stgImg = ImageTk.PhotoImage(img)
    label1.configure(image=stgImg)
    label1.image = stgImg
def Right_Window():
    global counter_second
    global img2
    counter_second += 1
    if counter_second > len(second_list)-1: counter_second = 0
    img2 = Image.open(second_list[counter_second]).convert('RGB')
    img2 = img2.resize((width, height))
    stgImg2 = ImageTk.PhotoImage(img2)
    label2.configure(image=stgImg2)
    label2.image = stgImg2
def Both_Left():
    Left_Window()
    Right_Window()
def Both_Right():
    global counter_first, counter_second, img, img2
    counter_first -= 1
    if counter_first < 0: counter_first = len(first_list)-1
    img = Image.open(first_list[counter_first]).convert('RGB')
    img = img.resize((width, height))
    stgImg = ImageTk.PhotoImage(img)
    label1.configure(image=stgImg)
    label1.image = stgImg
    counter_second -= 1
    if counter_second < 0: counter_second = len(second_list)-1
    img2 = Image.open(second_list[counter_second]).convert('RGB')
    img2 = img2.resize((width, height))
    stgImg2 = ImageTk.PhotoImage(img2)
    label2.configure(image=stgImg2)
    label2.image = stgImg2

def key_released(e):
    global counter_first
    if e.keycode == 37:
        Both_Left()
    if e.keycode == 39:
        Both_Right()
    show_diff()
    label4 = ttk.Label(text="Frame: " + str(counter_first))
    label4.grid(column=1, row=4, sticky="news")
    label4.configure()

root = Tk()
root.configure(bg='#BAC1F5',bd=0, highlightthickness=0)
frame = Frame(root, bg='black',highlightthickness=0)
frame.configure(bd=0, highlightthickness=0)
root.resizable(True, False)
root.state('zoomed')
color_checker_left = (0, 0, 0)
color_checker_right = (0, 0, 0)
def check_color():
    global color_checker_left
    global color_checker_right
    x, y = pyautogui.position()
    if x < (screen_width/2) - 4:
        color_checker_left = pyautogui.pixel(x, y)
        left_label = ttk.Label(text=str(color_checker_left))
        left_label.grid(column=0, row=1,sticky="news")
        left_label.configure()
        color_checker_right = pyautogui.pixel(int(((screen_width/2) + x)) + 4, y)
        right_label = ttk.Label(text=str(color_checker_right))
        right_label.grid(column=1, row=1,sticky="news")
        right_label.configure()
    elif x > (screen_width/2) + 4:
        color_checker_left = pyautogui.pixel(int((x - (screen_width/2))) - 4 , y)
        left_label = ttk.Label(text=str(color_checker_left))
        left_label.grid(column=0, row=1,sticky="news")
        left_label.configure()
        color_checker_right = pyautogui.pixel(x, y)
        right_label = ttk.Label(text=str(color_checker_right))
        right_label.grid(column=1, row=1,sticky="news")
        right_label.configure()
    root.after(100, check_color)


check_color()
img = Image.open(first_list[counter_first]).convert('RGB')
img = img.resize((width, height))
stgImg = ImageTk.PhotoImage(img)
label1 = ttk.Label(root, image=stgImg)
label1.grid(column=0, row=0,sticky="news")
img2 = Image.open(second_list[counter_second]).convert('RGB')
img2 = img2.resize((width, height))
stgImg2 = ImageTk.PhotoImage(img2)
label2 = ttk.Label(root, image=stgImg2)
label2.grid(column=1, row=0,sticky="news")
left_label = ttk.Label(text = str(color_checker_left))
left_label.grid(column=0, row=1,sticky="news")
right_label = ttk.Label(text = str(color_checker_right))
right_label.grid(column=2, row=1,sticky="news")

# columns = ('Frame', 'Differenece(MSE)')
# tree = ttk.Treeview(root, columns=columns, show='headings')
#
# tree.heading('Frame', text='Frame')
# tree.heading('Differenece(MSE)', text='Differenece(MSE)')
# for i in range(36):
#     tree.insert('', tk.END, values=str(i))
#
#
# tree.grid(column=1, row=4, sticky="ns")

label4 = ttk.Label(text ="Frame: " +  str(0))
label4.grid(column=1, row=4, sticky="news")

show_diff()

root.bind('<KeyRelease>',key_released )
root.mainloop()