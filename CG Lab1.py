import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
input_path = filedialog.askopenfilename()

img = Image.open(input_path).convert("RGB")
pixels = img.load()
width, height = img.size

pixels[0, 0] = (255, 127, 127)                   
pixels[width // 2, 0] = (127, 255, 127)          
pixels[0, height - 1] = (127, 127, 255)         

result_dir = "images"

result_path = os.path.join(result_dir, "result var 4.png")
img.save(result_path)

os.startfile(result_path)

"C:\Users\alex\Desktop\ВУЗ\Лабораторные работы\3 к 1 с\графика\Лаба 1\CG Lab 1\CG Lab1.py"