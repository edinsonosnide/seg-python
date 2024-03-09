import tkinter
import tkinter.messagebox
from tkinter import filedialog, ALL
import tkinter as tk
import customtkinter
from PIL import Image, ImageTk  # Asegúrate de tener instalada la biblioteca Pillow
import numpy as np

from PanZoomCanvas import PanZoomCanvas

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.imageUrl="a.jpg"
        self.file_path = "a.jpg"
        self.image = Image.open(self.file_path)

        # configure window
        self.title("GUI - Seeded Image Segmentation")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Welcome!", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.upload_image_button = customtkinter.CTkButton(self.sidebar_frame, command=self.upload_image_event, text="Upload Image")
        self.upload_image_button.grid(row=1, column=0, padx=20, pady=10)
        self.run_segmentation_button = customtkinter.CTkButton(self.sidebar_frame, command=self.run_segmentation_event, text="Run Segmentation")
        self.run_segmentation_button.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["100%", "90%", "80%", "70%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))



        # Cargar la imagen usando Pillow
        self.photoWidth = 450
        self.photoHeight = 350
        self.photo = customtkinter.CTkImage(light_image=Image.open(self.imageUrl),
                                          dark_image=Image.open(self.imageUrl),
                                          )



        self.a = PanZoomCanvas(master=self,  canvas_w=1024, canvas_h=768)
        self.a.set_image(self.file_path)



        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter message")
        self.entry.grid(row=5, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.send_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"),text="Send")
        self.send_button.grid(row=5, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250, height=100)
        self.textbox.grid(row=4, column=1, columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, rowspan=4, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Paint")
        self.tabview.add("Info")
        self.tabview.tab("Paint").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Info").grid_columnconfigure(0, weight=1)

        self.colors_optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Paint"), dynamic_resizing=False,
                                                        values=["None", "Red", "Yellow", "Green"], command=self.color_change_event)
        self.colors_optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.paint_it_button = customtkinter.CTkButton(self.tabview.tab("Paint"), text="Paint it",
                                                           command=self.paint_it_event)
        self.paint_it_button.grid(row=3, column=0, padx=20, pady=(10, 10))
        self.add_color_button = customtkinter.CTkButton(self.tabview.tab("Paint"), text="Add Color",
                                                           command=self.add_color_event)
        self.add_color_button.grid(row=4, column=0, padx=20, pady=(10, 10))

        self.imageNameInfo = customtkinter.CTkLabel(self.tabview.tab("Info"), text="Name = ")
        self.heightInfo = customtkinter.CTkLabel(self.tabview.tab("Info"), text="Hight = ")
        self.widthInfo = customtkinter.CTkLabel(self.tabview.tab("Info"), text="Width = ")
        self.imageNameInfo.grid(row=0, column=0, padx=20, pady=10)
        self.widthInfo.grid(row=1, column=0, padx=20, pady=5)
        self.heightInfo.grid(row=2, column=0, padx=20, pady=10)




    def paint_it_event(self):
        self.a.export_canvas_to_image()
        print("paint_it_button click")

    def add_color_event(self):
        print("add_color_button click")

    def color_change_event(self,chosen_color):
        print(chosen_color)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def upload_image_event(self):
        print("upload_image_event click")

        self.file_path = filedialog.askopenfilename(
            initialdir="C:/Users/edins/OneDrive/"
        )
        self.a.set_image(self.file_path)


    def run_segmentation_event(self):
        print("run_segmentation_event click")




if __name__ == "__main__":
    app = App()
    app.mainloop()