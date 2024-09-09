import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re


# fix file name error
def clean_filename(filename):
    # replaces invalide elements from the url 
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# download function
def download_image(img_url, folder):
    try:
        # get img
        filename = img_url.split('/')[-1]
        if not filename:
            filename = 'default_filename'
        
        # fix the name
        safe_filename = clean_filename(filename)
        
        # path
        filepath = os.path.join(folder, safe_filename)
        
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
        
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded: {filepath}")
        else:
            print(f"Failed to retrieve image from {img_url}")
    except Exception as e:
        print(f"An error occurred while downloading the image {img_url}: {e}")

# get imgs
def download_images_from_page(page_url, folder='images'):
    if not os.path.exists(folder):
        os.makedirs(folder)

    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage: {page_url}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img')

    if not img_tags:
        print("No images found on the webpage.")
        return

    for img in img_tags:
        img_url = img.get('src')
        if img_url:
            img_url = urljoin(page_url, img_url)
            download_image(img_url, folder)

# main 
if __name__ == '__main__':
    webpage_url = input("Enter the webpage URL: ")
    download_images_from_page(webpage_url)
# this's still a work in progress and it only works on public images.
