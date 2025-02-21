
import os
from PIL import Image
import numpy as np
import ttkbootstrap as ttk
from tkinter import filedialog

def open_file():
    file_path = filedialog.askopenfilename(
        title='Select a file',
        filetypes=[("Images", "*.png;*.jpg;*.jpeg")]
    )
    if file_path:
        generate_img(file_path)
    window.destroy()

def generate_img(file_path: str) -> None:

    ilumitaion_values: str = 'Ñ@#W$9876543210?!abc:;+=-,._   '[::-1]
    terminal_res: tuple = os.get_terminal_size()
    width, height = terminal_res

    os.system('cls')

    original_image = Image.open(file_path)
    new_image = original_image.resize(terminal_res, Image.Resampling.LANCZOS)

    linspace_rgb = list(np.linspace(0, 255, len(ilumitaion_values), dtype=np.integer))

    pixels = new_image.load()

    def get_ilum_value(rgb: tuple) -> str:
        avg: int = np.mean(rgb[:3])
        val: int = min(linspace_rgb, key=lambda x: abs(x - avg))
        return ilumitaion_values[linspace_rgb.index(val)]

    for x in range(height):
        for y in range(width):
            print(get_ilum_value(pixels[y, x]), end='')

window = ttk.Window(themename='darkly')
window.geometry('200x100')

button = ttk.Button(window, text='Choose a file', command=open_file).pack(pady=20)

window.mainloop()
