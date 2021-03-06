#Imports 
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import urllib.parse

from time import sleep
from random import randint

#Import product.py
from modules.product import get_product_url

def get_product_cat_url(catUrl):
    #Initiate Data Storage
    urls = []

    #Automated Pagination
    print("*****************************")
    print("New category URL for scraping")
    print(catUrl)

    #Find "Next" class in catURl
    print("Next class in category URL")
    req = requests.get(catUrl)
    soup = BeautifulSoup(req.content, "html.parser")

    nextClass = soup.find('li', class_="next")
    print(nextClass)

    if nextClass:
        #concatenate url
        cCatUrl = urllib.parse.urljoin(catUrl, 'page-')
        print("Several category pages found.")

        #Pagination 
        pages = np.arange(1,50,1)
        for page in pages:
            page = requests.get(cCatUrl + str(page) + ".html")
            soup = BeautifulSoup(page.text, "html.parser")

            #Condition for pagination.
            next = soup.find('li', class_="next")
            print(next)

            if next:
                print("New category page found..")
                #find all articles on category page
                articleClass = soup.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

                #Sleep to simulate a human
                sleep(randint(2,20))

                #Loop through each article
                for article in articleClass:
                    #Url 
                    bookUrlCat = article.article.h3.a.get("href")
                    #Join url
                    basicUrl = "https://books.toscrape.com/catalogue/category/books/princess-between-worlds-wide-awake-princess-5_919/index.html"
                    url = urllib.parse.urljoin(basicUrl, bookUrlCat)
                    urls.append(url)
            else:
                print("No new category found..")
                #find all article on last page
                articleClass = soup.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

                #Sleep to simulate a human
                sleep(randint(2,20))

                #Loop through each article
                for article in articleClass:
                    #Url 
                    bookUrlCat = article.article.h3.a.get("href")
                    #Join url
                    basicUrl = "https://books.toscrape.com/catalogue/category/books/princess-between-worlds-wide-awake-princess-5_919/index.html"
                    url = urllib.parse.urljoin(basicUrl, bookUrlCat)
                    urls.append(url)
                print("Last category page has been scraped.")
                break
    else:
        print("No several category pages found.")

        #find all articles on single category page.
        articleClass = soup.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

        #Sleep to simulate a human
        sleep(randint(2,20))

        #Loop through each article
        for article in articleClass:
            #Url 
            bookUrlCat = article.article.h3.a.get("href")
            #Join url
            basicUrl = "https://books.toscrape.com/catalogue/category/books/princess-between-worlds-wide-awake-princess-5_919/index.html"
            url = urllib.parse.urljoin(basicUrl, bookUrlCat)
            urls.append(url)
        print("Single Category page has been scraped")
        
    ### PRODUCT DATA LOOP

    #Initiate Data storage for books Infos
    bookInfos = []

    for link in urls:
        print (link)
        #Get Function
        productInfos = get_product_url(link)
        #Append Data in bookInfos
        bookInfos.append(productInfos)

    #Pandas DataFrame 
    dfBooks = pd.DataFrame(bookInfos)
        
    #Initiate category's name for csv file. 
    categoryName = soup.find("div", class_="page-header action").h1.text
    category ="%s_books.csv" % categoryName
    print("Save Data in : ")
    print(category)

    #To see data frame
    print(dfBooks)

    #to see datatypes of columns
    #print(dfBooks.dtypes)

    #to see where we're missing data & how much data is missing
    #print(dfBooks.isnull().sum())

    #move scraped data into a csv file name 'category_books.csv'
    dfBooks.to_csv('csv/' + category, encoding="utf-8-sig")

#get_product_cat_url("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")