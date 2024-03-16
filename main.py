import tkinter
import tkinter.messagebox
from copy import copy
from tkinter import filedialog, ALL
import tkinter as tk
import customtkinter
from PIL import Image,ImageTk
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

from isodata import isodataAlgo
from thresholding import algoThresholding
from k_means import algoKMeans

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #important variables
        self.file_path = "" # path to nifti file
        self.image_showing_path = "./images/canvas.png" # image showing on canvas
        self.current_data = None # nifti file loaded and gotten data with get_fdata()
        self.history_data = [] # all data gotten with get_fdata(), the first beign the original data
        self.image = None
        self.inital_slice = 0
        self.current_slice = self.inital_slice

        # creation of canvas
        self.canvas = tk.Canvas(self.master, width=512, height=512)
        self.canvas.grid(row=0, column=1, padx=20, pady=(20,20))
        self.canvas.create_image(0,0,anchor=tk.NW,image = self.image)

        # Configura los eventos del mouse
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw_on_image)

        self.start_x = None
        self.start_y = None


        self.current_color = "Red"
        self.annotationsCoordinates =  [] #example [ ([1,2,3,400), ([1,2,3,400), ([1,2,3,5000)] -> ([slice,slice,slice],intentisity of point)
        self.current_view_mode = "Coronal"

        # configure window
        self.title("GUI - Medical Images Segmentation")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.geometry("+0+0")  # Set the window position to the top-left corner

        # configure grid layout, only column one expands
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2,3,4,5), weight=1)

        # create sidebar frame with widgets
        self.left_sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.left_sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
        self.left_sidebar_frame.grid_rowconfigure(10, weight=1)

        # welcome text
        self.logo_label = customtkinter.CTkLabel(self.left_sidebar_frame, text="Welcome!", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # upload file button
        self.upload_image_button = customtkinter.CTkButton(self.left_sidebar_frame, command=self.upload_file_and_show_first_image_event, text="Upload NIFTI")
        self.upload_image_button.grid(row=1, column=0, padx=20, pady=10)

        # welcome text
        self.algos_label = customtkinter.CTkLabel(self.left_sidebar_frame, text="Avaliable Algos:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.algos_label.grid(row=2, column=0, padx=20, pady=(20, 10))

        # run_segmentation_button button
        self.run_thresholding_button = customtkinter.CTkButton(self.left_sidebar_frame, command=self.run_thresholding_event, text="Run Thresholding")
        self.run_thresholding_button.grid(row=4, column=0, padx=20, pady=10)

        # run_segmentation_button button
        self.run_isodata_button = customtkinter.CTkButton(self.left_sidebar_frame, command=self.run_isodata_event, text="Run Isodata")
        self.run_isodata_button.grid(row=5, column=0, padx=20, pady=10)

        # run_segmentation_button button
        self.run_region_growing_button = customtkinter.CTkButton(self.left_sidebar_frame, command=self.run_region_growing_event, text="Run Region Growing")
        self.run_region_growing_button.grid(row=6, column=0, padx=20, pady=10)

        # run_segmentation_button button
        self.run_k_means_button = customtkinter.CTkButton(self.left_sidebar_frame, command=self.run_k_means_event, text="Run K Means")
        self.run_k_means_button.grid(row=7, column=0, padx=20, pady=10)

        # appareance mode label
        self.appearance_mode_label = customtkinter.CTkLabel(self.left_sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=10)
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.left_sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))




        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, rowspan=4, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Paint")
        self.tabview.add("Info")
        self.tabview.tab("Paint").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Info").grid_columnconfigure(0, weight=1)

        # choose color text
        self.choose_color_label = customtkinter.CTkLabel(self.tabview.tab("Paint"), text="Choose a color:", font=customtkinter.CTkFont(size=20, weight="normal"))
        self.choose_color_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        #color options
        self.colors_optionmenu = customtkinter.CTkOptionMenu(self.tabview.tab("Paint"), dynamic_resizing=False,
                                                        values=["Red", "Yellow", "Green"], command=self.color_change_event)
        self.colors_optionmenu.grid(row=1, column=0, padx=20, pady=(20, 10))

        # choose color text
        self.choose_view_label = customtkinter.CTkLabel(self.tabview.tab("Paint"), text="Choose a view:", font=customtkinter.CTkFont(size=20, weight="normal"))
        self.choose_view_label.grid(row=2, column=0, padx=20, pady=(20, 10))

        #view mode of the file
        self.view_optionmenu = customtkinter.CTkOptionMenu(self.tabview.tab("Paint"), dynamic_resizing=False,
                                                        values=["Coronal", "Sagital", "Axial"], command=self.change_view_event)
        self.view_optionmenu.grid(row=3, column=0, padx=20, pady=(20, 10))

        # Slice view f the file
        self.label = customtkinter.CTkLabel(self.tabview.tab("Paint"), text="Current Slice: 0")
        self.label.grid(row=4, column=0, padx=20, pady=(20, 0))

        self.slider = customtkinter.CTkSlider(self.tabview.tab("Paint"), from_=0, to=0,  command=self.update_label,width=120)
        self.slider.grid(row=5, column=0, padx=20, pady=(0, 20))



        # Creamos un frame interno
        self.back_forth_buttons_frame = tk.Frame(self.tabview.tab("Paint"), bg=self.tabview.tab("Paint")._bg_color, width=350, height=150)
        self.back_forth_buttons_frame.grid(row=6, column=0, padx=0, pady=(20, 20))

        self.button_back = tk.Button(self.back_forth_buttons_frame, width=20)
        self.img_back = tk.PhotoImage(file="./images/go-back.png")  # asegúrate de usar "/" en lugar de "\"
        # Redimensionamos la imagen
        self.resized_img_back = self.img_back.subsample(20, 20)  # Ajusta los factores para redimensionar
        self.button_back.config(image=self.resized_img_back)
        self.button_back.grid(row=0, column=0, padx=(5, 5))

        self.button_forth = tk.Button(self.back_forth_buttons_frame, width=20)
        self.img_forth = tk.PhotoImage(file="./images/go-forth.png")  # asegúrate de usar "/" en lugar de "\"
        # Redimensionamos la imagen
        self.resized_img_forth = self.img_forth.subsample(20, 20)  # Ajusta los factores para redimensionar
        self.button_forth.config(image=self.resized_img_forth)
        self.button_forth.grid(row=0, column=1, padx=(5, 5),)

        # run_segmentation_button button
        self.clear_history_button = customtkinter.CTkButton(self.tabview.tab("Paint"), command=self.printing, text="Clear History")
        self.clear_history_button.grid(row=7, column=0, padx=20, pady=20)

    def printing(self):
        print("sfsfsd")

    def update_label(self, value):
        self.label.configure(text="Current Slice: {}".format(int(value)))
        self.current_slice = int(value)

        print(self.current_view_mode)
        # Create figure and axes
        '''
        IMPORTANT: THIS FUNCTION RESIZES THE ACTUAL DATA, IN SAVEFIG, I AM CROPPING THE BLANCK FRAME
        -> fig.savefig("./images/canvas.png", bbox_inches='tight', pad_inches=0)  # Adjust bounding box
        TO TRANSLATE THE DRAWINGS COORDINATES, THE WIDTH, HEIGHT, OF THE SAVED IMAGE MUST BE DIVIDED BY THE WIDTH, HEIGHT
        OF THE DATA.SHAPE[0], DATA.SHAPE[1] AND THEN DIVIE THE RESULT WITH WIDTH, HEIGHT OF EACH COORD OF THE DRAWINGS
        '''
        fig, axes = plt.subplots(1, 1, figsize=(8, 8),dpi=100)

        # Remove innnecesario info
        axes.axis('off')



        # Display initial slices
        ax0_img = None
        if self.current_view_mode == 'Coronal':
            ax0_img = axes.imshow(self.current_data[self.current_slice, :, :])
        elif self.current_view_mode == 'Sagital':
            ax0_img = axes.imshow(self.current_data[:, self.current_slice, :])
        elif self.current_view_mode == 'Axial':
            ax0_img = axes.imshow(self.current_data[:, :, self.current_slice])


        # Save the figure
        fig.savefig("./images/canvas.png", bbox_inches='tight', pad_inches=0)  # Adjust bounding box

        self.image = ImageTk.PhotoImage(file=self.image_showing_path)

        self.canvas.create_image(0,0,anchor=tk.NW,image = self.image)

        self.canvas.config(width=self.image.width(), height=self.image.height())
        self.canvas.update()

    def start_drawing(self, event):
        # Guarda las coordenadas iniciales del dibujo
        self.start_x = event.x
        self.start_y = event.y

    def draw_on_image(self, event):
        # Dibuja una línea desde las coordenadas iniciales hasta las coordenadas actuales
        if self.start_x is not None and self.start_y is not None:
            x, y = event.x, event.y
            self.canvas.create_oval(self.start_x, self.start_y,self.start_x, self.start_y, outline=self.current_color.lower(), width=2)
            self.start_x = x
            self.start_y = y
            print(self.start_x, self.start_y)


    def color_change_event(self,chosen_color):
        print(chosen_color)
        self.current_color = chosen_color

    def change_view_event(self, view_mode):
        print(view_mode)
        # Create figure and axes
        '''
        IMPORTANT: THIS FUNCTION RESIZES THE ACTUAL DATA, IN SAVEFIG, I AM CROPPING THE BLANCK FRAME
        -> fig.savefig("./images/canvas.png", bbox_inches='tight', pad_inches=0)  # Adjust bounding box
        TO TRANSLATE THE DRAWINGS COORDINATES, THE WIDTH, HEIGHT, OF THE SAVED IMAGE MUST BE DIVIDED BY THE WIDTH, HEIGHT
        OF THE DATA.SHAPE[0], DATA.SHAPE[1] AND THEN DIVIE THE RESULT WITH WIDTH, HEIGHT OF EACH COORD OF THE DRAWINGS
        '''
        fig, axes = plt.subplots(1, 1, figsize=(8, 8),dpi=100)

        # Remove innnecesario info
        axes.axis('off')

        self.current_view_mode = view_mode

        # Display initial slices
        ax0_img = None
        if view_mode == 'Coronal':
            # Reset the current slice
            self.slider.destroy()
            self.slider = customtkinter.CTkSlider(self.tabview.tab("Paint"), from_= 0,to=self.current_data.shape[0], command=self.update_label,
                                                  width=120)
            self.slider.grid(row=5, column=0, padx=20, pady=(0, 20))
            self.update_label(self.current_data.shape[0] // 2)
            ax0_img = axes.imshow(self.current_data[self.current_slice, :, :])
        elif view_mode == 'Sagital':
            # Reset the current slice
            self.slider.destroy()
            self.slider = customtkinter.CTkSlider(self.tabview.tab("Paint"), from_= 0,to=self.current_data.shape[1], command=self.update_label,
                                                  width=120)
            self.slider.grid(row=5, column=0, padx=20, pady=(0, 20))
            self.update_label(self.current_data.shape[1] // 2)
            ax0_img = axes.imshow(self.current_data[:, self.current_slice, :])
        elif view_mode == 'Axial':
            # Reset the current slice
            self.slider.destroy()
            self.slider = customtkinter.CTkSlider(self.tabview.tab("Paint"), from_= 0,to=self.current_data.shape[2], command=self.update_label,
                                                  width=120)
            self.slider.grid(row=5, column=0, padx=20, pady=(0, 20))
            self.update_label(self.current_data.shape[2] // 2)
            ax0_img = axes.imshow(self.current_data[:, :, self.current_slice])


        # Save the figure
        fig.savefig("./images/canvas.png", bbox_inches='tight', pad_inches=0)  # Adjust bounding box

        self.image = ImageTk.PhotoImage(file=self.image_showing_path)

        self.canvas.create_image(0,0,anchor=tk.NW,image = self.image)

        self.canvas.config(width=self.image.width(), height=self.image.height())
        self.canvas.update()



    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


    def upload_file_and_show_first_image_event(self):
        print("upload_file_event click")

        self.file_path = filedialog.askopenfilename(
            initialdir="C:/Users/edins/OneDrive/"
        )

        img_aux = nib.load(self.file_path)
        self.current_data = img_aux.get_fdata()
        print(self.current_data.shape)

        self.change_view_event("Coronal")

        self.history_data.append(self.current_data)

        self.save_image_paint_canvas()

        # Create figure and axes

    def save_image_paint_canvas(self):
        '''
        IMPORTANT: THIS FUNCTION RESIZES THE ACTUAL DATA, IN SAVEFIG, I AM CROPPING THE BLANCK FRAME
        -> fig.savefig("./images/canvas.png", bbox_inches='tight', pad_inches=0)  # Adjust bounding box
        TO TRANSLATE THE DRAWINGS COORDINATES, THE WIDTH, HEIGHT, OF THE SAVED IMAGE MUST BE DIVIDED BY THE WIDTH, HEIGHT
        OF THE DATA.SHAPE[0], DATA.SHAPE[1] AND THEN DIVIE THE RESULT WITH WIDTH, HEIGHT OF EACH COORD OF THE DRAWINGS
        '''
        fig, axes = plt.subplots(1, 1, figsize=(8, 8),dpi=100)


        # Remove innnecesario info
        axes.axis('off')

        # Display initial slices
        ax0_img = axes.imshow(self.current_data[self.current_slice, :, :])

        # Save the figure
        fig.savefig(self.image_showing_path, bbox_inches='tight', pad_inches=0)  # Adjust bounding box

        self.image = ImageTk.PhotoImage(file=self.image_showing_path)

        self.canvas.create_image(0,0,anchor=tk.NW,image = self.image)

        self.canvas.config(width=self.image.width(), height=self.image.height())
        self.canvas.update()

    def run_thresholding_event(self):
        print("run_thresholding_event click")
        tau_input = customtkinter.CTkInputDialog(text="Type in a tau:", title="Tau dialog")
        input_value = tau_input.get_input()
        try:
            # Convert the input to an integer
            tau_value = int(input_value)
            # Call the thresholding function with the current data and the user-provided threshold
            new_data = algoThresholding(copy(self.current_data), tau_value)
            self.current_data = new_data
            self.history_data.append(new_data)
            self.save_image_paint_canvas()
        except ValueError:
            print("Invalid input: Please enter an integer value for tau.")
    '''
    IMPORTANT:
        THERE MUST BE A FUNCTION THAT CHECKS THAT SELF.CURRENT_DATA IS NOT ONLY TRUE AND FALSE
    '''
    def run_isodata_event(self):
        print("run_isodata_event click")
        print("An example of what is inside of data is: ",str(self.current_data[0][0][0]))
        if str(self.current_data[0][0][0]) != 'False' and str(self.current_data[0][0][0]) != 'True':
            new_data = isodataAlgo(copy(self.current_data))
            self.current_data = new_data
            self.history_data.append(new_data)
            self.save_image_paint_canvas()


    def run_region_growing_event(self):
        print("run_region_growing_event click")

    def run_k_means_event(self):
        print("run_k_means_event click")
        clusters_input = customtkinter.CTkInputDialog(text="Type in the number of clusters:", title="Clusters dialog")
        input_value = clusters_input.get_input()
        try:
            # Convert the input to an integer
            clusters_value = int(input_value)
            # Call the thresholding function with the current data and the user-provided threshold
            new_data = algoKMeans(copy(self.current_data), clusters_value)
            self.current_data = new_data
            self.history_data.append(new_data)
            self.save_image_paint_canvas()
        except ValueError:
            print("Invalid input: Please enter an integer value for tau.")


if __name__ == "__main__":
    app = App()
    app.mainloop()