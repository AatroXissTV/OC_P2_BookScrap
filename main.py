#Imports
import requests
from requests import get
from bs4 import BeautifulSoup
import urllib.parse

from time import sleep
from random import randint

#Import category.py
from modules.category import get_product_cat_url

#Initiate Data Storage
catUrl = []

#Main Page url
mpUrl = "https://books.toscrape.com/index.html"
req = requests.get(mpUrl)
soup = BeautifulSoup(req.content, "html.parser")

#Extract Nav links list
navLink = soup.find('ul', class_="nav nav-list").li.ul
catNavLink = navLink.find_all('li')

#Loop in navlink list
for link in catNavLink:
    #Find all a.
    url = link.find('a').get('href')

    #Concatenate Url
    basicCatUrl = "https://books.toscrape.com/"
    finalCatUrl = urllib.parse.urljoin(basicCatUrl, url)
    #Append final Url in catUrl list.
    catUrl.append(finalCatUrl)

    #Get function
    categoryInfos = get_product_cat_url(finalCatUrl)
    print("A category has been Scraped")

print(catUrl)