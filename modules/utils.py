#Imports
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse


#Function : Download image
def download(url, folder):
    # if path doesn't exist, make that path dir
    if not os.path.isdir(folder):
        os.makedirs(folder)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    fileSize = int(response.headers.get("Content-Length", 0))
    # get the file name
    fileName = os.path.join(folder, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {fileName}", total=fileSize, unit="B", unit_scale=True, unit_divisor=1024)
    with open(fileName, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))
    
#download("https://books.toscrape.com/media/cache/db/01/db01b38d3200a5faff4ead42791416e4.jpg", "img")
