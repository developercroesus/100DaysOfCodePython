import requests
from bs4 import BeautifulSoup
from inputs import zillow_url, headers, form_url
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

response = requests.get(zillow_url, headers=headers)
time.sleep(2)
soup = BeautifulSoup(response.text, 'html.parser')
# new_list = [new_item for item in list if test]
result_count = soup.find(class_="result-count")
print(result_count.text)

CHROME_DRIVER_PATH = "C:\\Development\\chromedriver.exe"


def get_prices() -> list:
    prices = []
    spans = soup.find_all("span")
    for span in spans:
        try:
            if span['data-test'] == 'property-card-price':
                prices.append(span.text[0:6])
        except KeyError:
            pass
    return prices


def get_addresses():
    addresses_list = [address.text for address in soup.find_all('address')]
    addresses = []
    for address in addresses_list:
        try:
            addresses.append(address.split('|')[1])
        except IndexError:
            addresses.append(address)
    return addresses


def get_links():
    temp_link = ""
    links = []
    links_list = [link for link in soup.find_all('a', class_='property-card-link')]
    for link in links_list:
        if temp_link != link['href']:
            if link['href'][0] == '/':
                links.append("https://www.zillow.com" + link['href'])
            else:
                links.append(link['href'])
            temp_link = link['href']
    return links


def get_listings():
    addresses = get_addresses()
    prices = get_prices()
    links = get_links()
    # New_dict ={new_index, new_value for (index, value) in dict.items() if test}
    listings = []
    count = 1

    for index in range(len(addresses)):
        listing = {
            'id': count,
            'address': addresses[index],
            'price': prices[index],
            'link': links[index],
        }
        count += 1
        listings.append(listing)

    return listings

class FormFiller:
    """A call for filling in a Google form"""

    def __init__(self):
        self.service = Service('/Development/chromedriver')
        self.service.start()
        self.driver = webdriver.Remote(self.service.service_url)
        self.driver.maximize_window()

    def fill_form(self):
        self.driver.get(form_url)
        listings = get_listings()
        for listing in listings:
            time.sleep(1)
            add_address = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            add_address.send_keys(listing['address'])
            time.sleep(1)
            add_price = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            add_price.send_keys(listing['price'])
            time.sleep(1)
            add_link = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            add_link.send_keys(listing['link'])
            time.sleep(1)
            submit_button = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
            submit_button.click()
            time.sleep(1)
            another = self.driver.find_element(By.LINK_TEXT, 'Submit another response')
            another.click()
            time.sleep(1)

    def quit(self):
        time.sleep(600)
        self.driver.quit()

# TODO Use Selenium to fill in the form you created (step 1,2,3 above). Each listing should have its
#  price/address/link added to the form. You will need to fill in a new form for each new listing.

# TODO Once all the data has been filled in, click on the "Sheet" icon to create a Google Sheet from the responses to
#  the Google Form. You should end up with a spreadsheet with all the details from the properties.


open_form = FormFiller()
open_form.fill_form()
open_form.quit()
