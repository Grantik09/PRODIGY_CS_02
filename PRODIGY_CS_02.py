from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

def load_image(image_path):
    img = Image.open(image_path)
    return ImageTk.PhotoImage(img)

def encrypt_image(image_path, key):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            r = (r + key) % 256
            g = (g + key) % 256
            b = (b + key) % 256
            pixels[i, j] = (r, g, b)

    return img

def decrypt_image(image_path, key):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            r = (r - key) % 256
            g = (g - key) % 256
            b = (b - key) % 256
            pixels[i, j] = (r, g, b)

    return img

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        return file_path
    else:
        messagebox.showerror("Error", "No file selected.")
        return None

def save_file(img):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("BMP Files", "*.bmp")])
    if file_path:
        img.save(file_path)
        return file_path
    else:
        messagebox.showerror("Error", "No file selected.")
        return None

def show_image(image_path, label):
    img = Image.open(image_path)
    img = img.resize((250, 250))  # Resize to fit in the GUI
    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)
    label.image = photo

def encrypt_action():
    file_path = open_file()
    if file_path:
        try:
            key = int(key_entry.get())
            if 0 <= key <= 255:
                show_image(file_path, original_image_label)  # Show original image
                encrypted_img = encrypt_image(file_path, key)
                save_path = save_file(encrypted_img)
                if save_path:
                    show_image(save_path, result_image_label)  # Show encrypted image
                    messagebox.showinfo("Success", "Image encrypted successfully.")
            else:
                messagebox.showerror("Error", "Key must be between 0 and 255.")
        except ValueError:
            messagebox.showerror("Error", "Invalid key. Please enter a number.")

def decrypt_action():
    file_path = open_file()
    if file_path:
        try:
            key = int(key_entry.get())
            if 0 <= key <= 255:
                show_image(file_path, original_image_label)  # Show original image
                decrypted_img = decrypt_image(file_path, key)
                save_path = save_file(decrypted_img)
                if save_path:
                    show_image(save_path, result_image_label)  # Show decrypted image
                    messagebox.showinfo("Success", "Image decrypted successfully.")
            else:
                messagebox.showerror("Error", "Key must be between 0 and 255.")
        except ValueError:
            messagebox.showerror("Error", "Invalid key. Please enter a number.")

# Create GUI
root = tk.Tk()
root.title("Image Encryption Tool")

tk.Label(root, text="Enter Key (0-255):").pack(pady=10)
key_entry = tk.Entry(root)
key_entry.pack(pady=5)

tk.Button(root, text="Encrypt Image", command=encrypt_action).pack(pady=10)
tk.Button(root, text="Decrypt Image", command=decrypt_action).pack(pady=10)

# Labels for displaying images
original_image_label = tk.Label(root, text="Original Image")
original_image_label.pack(pady=10)

result_image_label = tk.Label(root, text="Result Image")
result_image_label.pack(pady=10)

root.mainloop()
