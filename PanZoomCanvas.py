import tkinter
import tkinter.messagebox
from tkinter import filedialog, ALL
import tkinter as tk
import customtkinter
from PIL import Image, ImageTk, ImageDraw  # Asegúrate de tener instalada la biblioteca Pillow
import numpy as np
import os

import io
class PanZoomCanvas(tk.Frame):
    def __init__(self, master, canvas_w, canvas_h):
        super().__init__(master)
        self.pil_image = None  # Image data to be displayed

        self.pen_size = 5
        self.zoom_cycle = 0

        self.create_widget(canvas_w, canvas_h)  # Create canvas


    # Define the create_widget method.
    def create_widget(self, width, height):
        # Canvas
        self.canvas = tk.Canvas(self.master, background="blue", width=width, height=height)
        self.canvas.grid(row=0, column=1, padx=20, pady=(20,20))





        self.canvas.bind("<B3-Motion>", self.draw_ovals)


    def export_canvas_to_image(self):
        filename = "PanZoomCanvas"

        myps = self.canvas.postscript(file=filename+".eps",colormode='color')




        # Save the image as a JPEG file (you can choose a different format if needed)
        #img.save('test.jpg')
        #img = Image.open(filename+".eps")
        #img.save(filename+".png",format="png")

        #os.remove(filename+".ps")

    def draw_ovals(self,event):
        print("aaaaa")
        x1, y1 = (event.x - self.pen_size), (event.y-self.pen_size)
        x2, y2 = (event.x + self.pen_size), (event.y-self.pen_size)
        self.canvas.create_oval(x1, y1, x2, y2)

    def set_image(self, filename):



        '''To open an image file'''
        if not filename:
            return
        # PIL.Image
        self.pil_image = Image.open(filename)
        self.width = self.pil_image.width
        self.height = self.pil_image.height
        print(self.width,self.height)
        self.canvas.configure(width=self.width,height=self.height,background="blue")

        print(self.canvas.winfo_width(), self.canvas.winfo_height())
        # Set the affine transformation matrix to display the entire image.

        # To display the image
        self.draw_image(self.pil_image)

    # -------------------------------------------------------------------------------
    # Mouse events
    # -------------------------------------------------------------------------------





    # -------------------------------------------------------------------------------
    # Drawing
    # -------------------------------------------------------------------------------

    def draw_image(self, pil_image):

        if pil_image == None:
            return

        self.pil_image = pil_image

        # Canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()


        im = ImageTk.PhotoImage(image=pil_image)

        # Draw the image
        item = self.canvas.create_image(
            0, 0,  # Image display position (top-left coordinate)
            anchor='nw',  # Anchor, top-left is the origin
            image=im  # Display image data
        )
        self.image = im

    def redraw_image(self):
        '''Redraw the image'''
        if self.pil_image == None:
            return
        self.draw_image(self.pil_image)






