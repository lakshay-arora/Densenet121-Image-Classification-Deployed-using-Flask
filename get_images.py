# importing required libraries
import requests
from bs4 import BeautifulSoup
import os
import time

def get_directory(url):
    return "URL_" + str(url.replace("/","_"))

def get_path(url):
    return "static/URL_" + str(url.replace("/","_"))

headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }

def get_images(url):
    path = get_path(url)
    try:
        os.mkdir(path)
    except:
        pass
    response = requests.request("GET", url, headers=headers)
    data = BeautifulSoup(response.text, 'html.parser')
    images = data.find_all('img', src=True)
    print('Number of Images: ', len(images))
    # select src tag
    image_src = [x['src'] for x in images]
    # select only jp format images
    image_src = [x for x in image_src if x.endswith('.jpeg') ]
    image_count = 1
    for image in image_src:
        print(image)
        image_file_name = path+'/'+str(image_count)+'.jpeg' 
        print(image_file_name)
        with open(image_file_name, 'wb') as f:
            res = requests.get(image)
            f.write(res.content)
        image_count = image_count+1

