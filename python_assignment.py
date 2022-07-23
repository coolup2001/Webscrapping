#Importing libraries
import csv
from bs4 import BeautifulSoup

#Import webdriver
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions

#To start firefox use this
# driver = webdriver.FireFox()

#To start edge use this
# options = EdgeOptions()
# options.use_chrome = True
# driver = Edge(options=options)

#To start chrome use this
# driver = webdriver.Chrome()

#Getting to next page
def get_url():
    template = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
    url = template
    url+='&page'
    return url

#Extract record
def extract_record(item):
    """Extract and return data from a single record"""
    
    #For product name and url
    atag = item.h2.a
    product_name = atag.text.strip()
    product_url = 'https://www.amazon.in' + atag.get('href')
    try:
        #For product price
        price_parent = item.find('span', 'a-price')
        product_price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return
    
    try:
        #For product ratings
        rating = item.i.text
        #For number of review
        no_of_review = item.find('span', {'class': 'a-size-base'}).text
    except AttributeError:
        rating =''
        no_of_review = ''
        
    result = (product_url, product_name, product_price, rating, no_of_review)
    return result

# Creating main function
def main():
    driver = webdriver.Chrome()
    records = []
    url = get_url()
    for page in range(1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
    driver.close()
    
    #Export to csv
    with open('data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['product_url', 'product_name', 'product_price', 'rating', 'no_of_review'])
        writer.writerows(records)
main()