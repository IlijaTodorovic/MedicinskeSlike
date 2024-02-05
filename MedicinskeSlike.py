import tkinter as tk
from tkinter import filedialog
from PIL import Image ,ImageTk
import cv2
import pydicom.data
import pydicom
from pydicom.pixel_data_handlers import apply_voi_lut
import numpy as np
from matplotlib import cm

root=tk.Tk()
root.geometry("800x600")
root.title("MedicinskeSlike")

class GUI: 

    def __init__(self): 
        self.file_path = ""
        self.left_frame= tk.Frame(root, width=200, height=600, bg="white")
        self.left_frame.pack(side="left", fill="y")
        self.canvas = tk.Canvas(root, width=700, height=600)
        self.canvas.pack(padx= 30, pady=40)
        button = tk.Button(self.left_frame, text="Import DICOM", font=('Arial', 12) ,command = self.import_image)
        button.pack(padx=20, pady=20)
        button = tk.Button(self.left_frame, text="IZRACUNAJ", font=('Arial', 12) , command = self.racunaj_konture)
        button.pack(padx=20, pady=40)
        self.text=tk.Label(self.left_frame, text=f"")
        self.text.pack(padx=20, pady=20)

    def import_image(self):
        self.text.config(text="")
        self.file_path = filedialog.askopenfilename()
        if not self.file_path.endswith('.dcm'):
            self.text.config(text="slika mora da bude dcm formata")
            return
        dicom_image= pydicom.read_file(self.file_path) 
        slika_u_niz = apply_voi_lut(dicom_image.pixel_array, dicom_image) 
        slika_u_niz = slika_u_niz / slika_u_niz.max() 
        self.save_for_cont = slika_u_niz
        image = Image.fromarray(np.uint8(cm.gist_earth(slika_u_niz)*255)) 
        self.canvas.config(width=image.width, height=image.height) 
        image= ImageTk.PhotoImage(image) 
        self.canvas.image= image
        self.canvas.create_image(0,0, image=image, anchor="nw")

    def racunaj_konture(self):
        if self.file_path == "":
            self.text.config(text="moras prvo ucitati sliku ! ")
            return
        _, t1 = cv2.threshold(self.save_for_cont,0.55,1,cv2.THRESH_BINARY)
        t1 = t1.astype(np.uint8) 
        contours, _  = cv2.findContours(t1,1,2)
        area = cv2.contourArea(contours[0]) 
        t1 = t1.astype(np.float32) 
        image = Image.fromarray(np.uint8(cm.gist_earth(t1)*255)) 
        image= ImageTk.PhotoImage(image)
        self.canvas.image= image
        self.canvas.create_image(0,0 ,image=image, anchor="nw")
        self.text.config(text=f"Povrsina konture:{area}")


gui = GUI()

root.mainloop()