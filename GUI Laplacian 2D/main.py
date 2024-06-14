import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import factorized
import matplotlib.pyplot as plt

class ImageSegmentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Segmentation with Laplacian Coordinates")

        self.canvas = tk.Canvas(root, width=800, height=600, bg='gray')
        self.canvas.pack()

        self.foreground_seeds = []
        self.background_seeds = []
        self.current_label = 'F'  # Default to foreground
        self.painting = False  # Flag to track painting state

        self.image = None
        self.image_tk = None
        self.scale_factor = 1.0

        self.init_ui()

    def init_ui(self):
        # Load image button
        self.btn_load = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.btn_load.pack(side=tk.LEFT)

        # Select color buttons
        self.btn_foreground = tk.Button(self.root, text="Foreground (Red)", command=lambda: self.set_label('F'))
        self.btn_foreground.pack(side=tk.LEFT)
        
        self.btn_background = tk.Button(self.root, text="Background (Green)", command=lambda: self.set_label('B'))
        self.btn_background.pack(side=tk.LEFT)

        # Segment image button
        self.btn_segment = tk.Button(self.root, text="Segment Image", command=self.segment_image)
        self.btn_segment.pack(side=tk.LEFT)

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_paint)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.stop_paint)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path).convert('L')
            self.original_image = self.image.copy()

            # Calculate scale factor
            self.scale_factor = min(800 / self.image.width, 600 / self.image.height)

            # Resize image for display
            new_size = (int(self.image.width * self.scale_factor), int(self.image.height * self.scale_factor))
            self.image = self.image.resize(new_size, Image.LANCZOS)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            self.foreground_seeds.clear()
            self.background_seeds.clear()

    def set_label(self, label):
        self.current_label = label

    def start_paint(self, event):
        self.painting = True
        self.paint(event)

    def paint(self, event):
        if not self.painting:
            return

        # Adjust coordinates based on scale factor
        x = int(event.x / self.scale_factor)
        y = int(event.y / self.scale_factor)
        
        if self.current_label == 'F':
            self.foreground_seeds.append((y, x))
            color = 'red'
        else:
            self.background_seeds.append((y, x))
            color = 'green'

        # Draw on the canvas with the correct scale
        self.canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill=color, outline=color)

    def stop_paint(self, event):
        self.painting = False

    def calculate_weights(self, image, beta=0.001):
        height, width = image.shape
        num_pixels = height * width
        indices = np.arange(num_pixels).reshape(height, width)
        W = sp.lil_matrix((num_pixels, num_pixels))

        sigma = 0
        for i in range(height):
            for j in range(width):
                if i > 0: sigma = max(sigma, np.abs(image[i, j] - image[i - 1, j]))
                if i < height - 1: sigma = max(sigma, np.abs(image[i, j] - image[i + 1, j]))
                if j > 0: sigma = max(sigma, np.abs(image[i, j] - image[i, j - 1]))
                if j < width - 1: sigma = max(sigma, np.abs(image[i, j] - image[i, j + 1]))

        if sigma == 0: sigma = 1

        for i in range(height):
            for j in range(width):
                index = indices[i, j]
                if i > 0: W[index, indices[i - 1, j]] = np.exp(-beta * (np.abs(image[i, j] - image[i - 1, j]) / sigma))
                if i < height - 1: W[index, indices[i + 1, j]] = np.exp(-beta * (np.abs(image[i, j] - image[i + 1, j]) / sigma))
                if j > 0: W[index, indices[i, j - 1]] = np.exp(-beta * (np.abs(image[i, j] - image[i, j - 1]) / sigma))
                if j < width - 1: W[index, indices[i, j + 1]] = np.exp(-beta * (np.abs(image[i, j] - image[i, j + 1]) / sigma))

        return W.tocsr()

    def segment_image(self):
        if self.image is None or not self.foreground_seeds or not self.background_seeds:
            return

        image_array = np.array(self.original_image)
        height, width = image_array.shape
        num_pixels = height * width
        indices = np.arange(num_pixels).reshape(height, width)

        W = self.calculate_weights(image_array)
        D = np.array(W.sum(axis=1)).flatten()
        L = sp.diags(D) - W
        L2 = L.dot(L)

        I_s = sp.lil_matrix((num_pixels, num_pixels))
        b = np.zeros(num_pixels)

        for y, x in self.foreground_seeds:
            try:
                idx = indices[y, x]
                I_s[idx, idx] = 1
                b[idx] = 200  # Foreground value
            except:
                pass

        for y, x in self.background_seeds:
            try:
                idx = indices[y, x]
                I_s[idx, idx] = 1
                b[idx] = 0  # Background value
            except:
                pass

        A = I_s.tocsr() + L2
        solve = factorized(A)
        x = solve(b)
        segmented_image = x.reshape((height, width))

        # Apply labels for better visualization
        labeled_image = self.apply_labels(segmented_image, image_array, 200, 10)

        plt.imshow(labeled_image, cmap='gray')
        plt.title("Segmented Image")
        plt.show()

    def apply_labels(self, segmented_values, image, xB, xF):
        # Calcular el umbral basado en xB y xF
        threshold = (xB + xF) / 2

        # Asignar etiquetas basado en el umbral
        labels = np.where(segmented_values >= threshold, image, xF)

        return labels

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSegmentationApp(root)
    root.mainloop()
