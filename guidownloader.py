import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import tkinter as tk
from tkinter import filedialog, messagebox
# using tkinter to turn this into a GUI for ease of use :)
from PIL import Image, ImageTk
# to fix the window icon

# fix file name error
def clean_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# download function
def download_image(img_url, folder):
    try:
        filename = img_url.split('/')[-1]
        if not filename:
            filename = 'default_filename'
        
        safe_filename = clean_filename(filename)
        filepath = os.path.join(folder, safe_filename)
        
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"downloaded: {filepath}")
        else:
            print(f"failure to retrieve the images from {img_url}")
    except Exception as e:
        print(f"an error occurred while downloading the image {img_url}: {e}")

# get imgse
def download_images_from_page(page_url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    response = requests.get(page_url)
    if response.status_code != 200:
        messagebox.showerror("Error", f"Failed to retrieve the webpage: {page_url}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img')

    if not img_tags:
        messagebox.showinfo("Info", "No images found on the webpage.")
        return

    for img in img_tags:
        img_url = img.get('src')
        if img_url:
            img_url = urljoin(page_url, img_url)
            download_image(img_url, folder)

# start download + path
def start_download():
    url = url_entry.get()
    folder = folder_path.get()
    
    if not url or not folder:
        messagebox.showerror("Error", "Please enter both the webpage URL and the folder path.")
        return
    
    download_images_from_page(url, folder)
    messagebox.showinfo("Success", "Download complete!")

#  select folder + url
def start_download():
    url = url_entry.get()
    folder = folder_path.get()
    
    if not url or not folder:
        messagebox.showerror("Error", "insert both URL and folder path.")
        return
    
    download_images_from_page(url, folder)
    messagebox.showinfo("Success", "complete :D!")

# browse folder
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)

# tk window
root = tk.Tk()
root.title("Image Downloader")

# icon..
icon_path = r'C:\Users\DASH\Pictures\IMG\icon.png'
icon = tk.PhotoImage(file=icon_path)  
root.iconphoto(True, icon)

#  widgets (??)
tk.Label(root, text="Webpage URL:").pack(padx=10, pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(padx=10, pady=5)

tk.Label(root, text="Save Images To:").pack(padx=10, pady=5)
folder_path = tk.StringVar()
folder_entry = tk.Entry(root, textvariable=folder_path, width=50, state='readonly')
folder_entry.pack(padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_folder).pack(padx=10, pady=5)

tk.Button(root, text="Download Images", command=start_download).pack(padx=10, pady=10)

# GUI loop
root.mainloop()
# this's still a work in progress and it only works on public images.
# this version of the code contains a GUI incase using cmd is a hassle ^^'