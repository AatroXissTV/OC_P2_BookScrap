#Import BeautifulSoup, Requests & csv
import bs4
from bs4 import BeautifulSoup
import requests
import csv

#Insert the WebPage link here
url = "https://books.toscrape.com/catalogue/princess-between-worlds-wide-awake-princess-5_919/index.html"
#Extracting WebPage HTML and declare it as raw content
req = requests.get(url)
raw = req.content
#Parsing WebPage and making it a BeautifulSoup Object.
soup = BeautifulSoup(raw, "html.parser")


#Extracting product URL
bookUrl = [url]

#Extracting product Image
bookImageList = soup.find("div", class_= "item active").img
bookImage = [bookImageList.get("src")]

#Extracting product Title
bookTitleList = soup.find('h1').text
bookTitle = [bookTitleList]

#Extracting table Informations
#Getting table
table = soup.find('table', attrs={'class': 'table table-striped'})
rows = []
# Find all tr tags
tableRows = table.find_all('tr')

for row in tableRows:
    value = row.find_all('td')
    beautified_value = [ele.text.strip() for ele in value]
    rows.append(beautified_value)

#Extracting UPC
bookUpc = rows[0]

#Extracting Price Exc taxes
bookPriceWithoutTaxes = rows[2]

#Extracting Price Incl Taxes
bookPriceWithTaxes = rows[3]

#Extracting Availability
bookAvailability = rows[5]

#Extracting product Category
bookCategoryList = soup.find_all('li')[2].a
bookCategory = [bookCategoryList.string]

#Extracting product description
bookDescriptionList = soup.find("meta", attrs={"name":"description"})
bookDescription = [bookDescriptionList.get("content").strip()]

#Extracting Review Rating
bookRatingList = soup.find('p', {'class': 'star-rating'})['class'][1]
bookRating = [bookRatingList]

#Load all in a csv file
#Create a list for headings
headings = ["product_page__url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url" ]

#Create a new file in order to write in data.csv
with open("data.csv", "w") as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(headings)
    for product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url in zip(bookUrl,bookUpc,bookTitle,bookPriceWithTaxes,bookPriceWithoutTaxes,bookAvailability,bookDescription,bookCategory,bookRating, bookImage):
        writer.writerow([product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url])