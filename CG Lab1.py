import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox

class ImageProcessing:
    def __init__(self, root):
        self.root = root
        self.root.title("Обработка изображения")
        self.root.geometry("800x600")

        self.orig_img = None
        self.result_img = None
        self.display_img = None

        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.button_open = tk.Button(button_frame, text="Открыть", command=self.open_image, width=15, height=2)
        self.button_open.pack(side=tk.LEFT, padx=5)

        self.button_process = tk.Button(button_frame, text="Обработать", command=self.process_image, width=15, height=2, state=tk.DISABLED)
        self.button_process.pack(side=tk.LEFT, padx=5)

        self.button_save = tk.Button(button_frame, text="Сохранить", command=self.save_image, width=15, height=2, state=tk.DISABLED)
        self.button_save.pack(side=tk.LEFT, padx=5)

        self.image_label = tk.Label(root, text="Выберите изображение", bg="#e0e0e0")
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.button_save_pbm = tk.Button(button_frame, text="Сохранить в PBM", command=self.save_pbm, width=15, height=2, state=tk.DISABLED)
        self.button_save_pbm.pack(side=tk.LEFT, padx=5)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.webp"), ("Все файлы", "*.*")])
        if not file_path:
            return

        self.orig_img = Image.open(file_path).convert("RGB")
        self.result_img = None

        self.button_process.config(state=tk.NORMAL)
        self.button_save.config(state=tk.DISABLED)
        self.button_save_pbm.config(state=tk.DISABLED)

        self.show_image(self.orig_img)

    def process_image(self):
        if self.orig_img is None:
            return

        self.result_img = self.orig_img.copy()
        pixels = self.result_img.load()
        width, height = self.result_img.size

        pixels[0, 0] = (255, 127, 127) #левый верхний угол, насыщенный розовый
        pixels[width // 2, 0] = (127, 255, 127) #центр верхней строки, кричащий зелёный
        pixels[0, height - 1] = (127, 127, 255) #левый нижний угол, умеренный аспидно-синий

        self.show_image(self.result_img)
        self.button_save.config(state=tk.NORMAL)
        self.button_save_pbm.config(state=tk.NORMAL)
        messagebox.showinfo("Успех", "Изображение обработано!")

    def save_image(self):
        if self.result_img is None:
            return

        result_dir = "images"

        result_path = os.path.join(result_dir, "result var 4.png")
        self.result_img.save(result_path)
        messagebox.showinfo("Сохранение", f"Файл сохранен в:\n{os.path.abspath(result_path)}")

    def show_image(self, img):
        label_width = self.image_label.winfo_width()
        label_height = self.image_label.winfo_height()

        if label_width <= 1 or label_height <= 1:
            label_width, label_height = 700, 500

        img_copy = img.copy()
        img_copy.thumbnail((label_width, label_height), Image.Resampling.LANCZOS)

        self.display_img = ImageTk.PhotoImage(img_copy)
        self.image_label.config(image=self.display_img, text="")

    def save_pbm(self):
        if self.result_img is None:
            return

        result_dir = "images"
        
        result_path = os.path.join(result_dir, "result var 4.pbm")

        width, height = self.result_img.size
        pixels = self.result_img.load()

        with open(result_path, 'w', encoding='ascii') as f:
            f.write(f"{width} {height}\n")

            for y in range(height):
                row = []
                for x in range(width):
                    r, g, b = pixels[x, y]
                    brightness = (r + g + b) // 3
                    pixel_bin = 1 if brightness < 128 else 0
                    row.append(str(pixel_bin))

                f.write(" ".join(row) + "\n")

        messagebox.showinfo("Сохранение", f"Файл PBM сохранен в:\n{os.path.abspath(result_path)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessing(root)
    root.mainloop()