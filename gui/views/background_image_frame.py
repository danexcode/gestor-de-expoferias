import tkinter as tk
from PIL import Image, ImageTk
import os
import sys

class BackgroundImageFrame(tk.Frame):
    def __init__(self, master, background_image_filename="welcome_background.png", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.background_image_filename = background_image_filename
        self.photo_image = None

        self.background_label = tk.Label(self)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bind("<Configure>", self._on_resize)

    def _get_image_path(self):
        if hasattr(sys, '_MEIPASS'):
            base_dir = os.path.join(sys._MEIPASS, "assets")
        else:
            base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
        return os.path.join(base_dir, self.background_image_filename)

    def load_background_image(self, width, height):
        full_image_path = self._get_image_path()
        try:
            original_image = Image.open(full_image_path)
            resized_image = original_image.resize((width, height), Image.Resampling.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(resized_image)
            return self.photo_image
        except Exception as e:
            print(f"ERROR cargando imagen de fondo: {e}")
            return None

    def _on_resize(self, event):
        new_width = event.width
        new_height = event.height
        if new_width > 0 and new_height > 0:
            temp_image = self.load_background_image(new_width, new_height)
            if temp_image:
                self.background_label.config(image=temp_image)