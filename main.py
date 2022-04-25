from selenium impo




rt webdriver
from bs4 import BeautifulSoup
import pandas as pd
import json


def write_json(data, filename='json_file.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


df = pd.read_csv("Amazon Scraping.csv")
asin_list = df['Asin'].to_list()
country_list = df['country'].to_list()

chrome_driver_path = "C:/Users/amity/OneDrive/Desktop/Projects/python/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
data_file = []
for i in range(100):
    url = f"https://www.amazon.{country_list[i]}/dp/{asin_list[i]}"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        product_title = soup.find(id = 'productTitle')
        product_url = soup.find(id='landingImage')
        if product_url == None:
            product_url = soup.find(id = 'imgBlkFront')
        product_price = soup.find('span',{'class': 'a-offscreen'})
        if product_price ==None:
            product_price = soup.find('span',{'class': 'a-color-price'})
        product_details = soup.select('#feature-bullets > ul > li > span')
        if product_details ==[]:
            product_details = soup.select('#bookDescription_feature_div > div > div.a-expander-content.a-expander-partial-collapse-content > span')
        print(product_title.text, product_url['src'],product_price.text,product_details)
        data = {
            'product_title': product_title.text,
            'product_url': product_url['src'],
            'product_price': product_price.text,
            'product_details': product_details[0].text
        }
        data_file.append(data)
        print(data)
    except:
        print(url, 'not available.')
# driver.quit()
write_json(data_file)
