#Imports 
import requests
from requests import get
import bs4
from bs4 import BeautifulSoup
import urllib.parse
import re

#Import Download img
from modules.utils import download

def get_product_url(url): 
    #Initiate Data Storage
    bookUrl = ""
    bookImage = ""
    bookTitle = ""
    bookUpc = ""
    bookPriceWithVat = ""
    bookPriceWithoutVat = ""
    bookAvailability = ""
    bookCategory = ""
    bookDescription = ""
    bookRating = ""

    #DefaultUrl
    #url : taking function argument for request url
    #Extracting Page HTML -> convert in soup object
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")

    #Extract Data from product page

    #Url
    bookUrl = url

    #Image
    ImgUrl = soup.find("div", class_="item active").img.get('src')

    #Join url
    basicImgUrl = "https://books.toscrape.com/"
    finalImgUrl = urllib.parse.urljoin(basicImgUrl, ImgUrl)
    bookImage = finalImgUrl

    #get function
    download(bookImage, "img")

    #Title
    title = soup.find('h1').text
    bookTitle = title

    #Product Category
    category = soup.find_all('li')[2].a.string
    bookCategory = category

    #Product Description
    description = soup.find("meta", attrs={"name": "description"}).get("content").strip()
    bookDescription = description

    #Product Rating 
    rating = soup.find('p', {'class': 'star-rating'})['class'][1]
    bookRating = rating

    #Extract Data from Table
    # Step 1 : Getting Table 
    table = soup.find('table', attrs={'class': 'table table-striped'})
    #Setp 2 : Initiate Cells list
    rows = []
    #Step 3 : Get all trs
    tableRows = table.find_all('tr')
    #Step 4 : Loop in tablRows
    for row in tableRows:
        value = row.find_all('td')
        beautified_value = [ele.text.strip() for ele in value]
        rows.append(beautified_value)

    #Put Data in Data Storage
    #UPC
    bookUpc = rows[0][0]

    #Price Exc taxes
    bookPriceWithoutVat = rows[2][0]

    #Price inc taxes
    bookPriceWithVat = rows[3][0]

    #Book Availability
    string = rows[5][0]
    temp = re.findall(r'\d+', string)
    res = list(map(int, temp))
    for r in res:
        bookAvailability = r


    productInfos = {
        'product_page_url': bookUrl,
        'universal_product_code': bookUpc,
        'title': bookTitle,
        'price_including_tax': bookPriceWithVat,
        'price_excluding_tax': bookPriceWithoutVat,
        'number_available': bookAvailability,
        'product_description': bookDescription,
        'category': bookCategory,
        'review_rating': bookRating,
        'image_url': bookImage,
    }

    return productInfos

#get_product_url("https://books.toscrape.com/catalogue/princess-between-worlds-wide-awake-princess-5_919/index.html")