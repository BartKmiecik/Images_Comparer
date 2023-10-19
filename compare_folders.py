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
import pandas as pd

def error(img1, img2):
   img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
   img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
   diff = cv2.subtract(img1, img2)
   err = np.sum(diff**2)
   mse = err/(float(height*width))
   # msre = np.sqrt(mse)
   return mse, diff

# screen_width, screen_height = pyautogui.size()
width, height = 960, 540
references_images_directory = filedialog.askdirectory(title="Select Reference Folder")
renders_images_directory = filedialog.askdirectory(title="Select Renders Folder")
folder_one = Path(references_images_directory)
folder_two = Path(renders_images_directory)

# folder_one = Path('ToExclude/NBV_Org')
# folder_two = Path("ToExclude/NBV_Rend")

# for f in group_of_folders1:
#     print(os.path.basename(f))

group_of_folders1 = sorted(folder_one.glob("*"))
group_of_folders2 = sorted(folder_two.glob("*"))

main_data = {}

def _p_file_sort_key(file_path):
    return int(re.match(r"(\d+)", file_path.name[-6:].replace('_', '0')).group(1))

def compareColors(folder_one, folder_two):
    global main_data
    types = ("*.png", "*.jpg")
    first_list, second_list = [], []
    for typed in types:
        f1 = sorted(folder_one.glob(typed), key=_p_file_sort_key)
        if len(f1) > 0:
            first_list.extend(f1)
        f2 = sorted(folder_two.glob(typed), key=_p_file_sort_key)
        if len(f2) > 0:
            second_list.extend(f2)

    all_compared = []
    data = []

    for i in range(len(first_list)):
        img = Image.open(first_list[i]).convert('RGB')
        img = img.resize((width, height))
        img2 = Image.open(second_list[i]).convert('RGB')
        img2 = img2.resize((width, height))
        match_error12, diff12 = error(np.asarray(img), np.asarray(img2))
        data.append("{:.2f}".format(match_error12))
        # print("Image: " + str(first_list[i])[-6:] + " Image2: " + str(second_list[i])[-6:])
        # print("Frame " + str(i) + " MSE error: " + str(match_error12))
    car_paint = os.path.basename(folder_one)
    main_data[car_paint] = data
    # df = pd.DataFrame(main_data)
    # print(df)


for f in range(len(group_of_folders1)):
    compareColors(group_of_folders1[f], group_of_folders2[f])

df = pd.DataFrame(main_data)
df.to_csv("Juke.csv")