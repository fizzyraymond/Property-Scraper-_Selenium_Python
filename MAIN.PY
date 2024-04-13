import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time


# URL of the page to scrape
url = "ENTER FULL URL HERE"

# Send an HTTP request to the URL
response = requests.get(url)
response.raise_for_status()  # Will raise an exception for bad requests (400 or 500 error codes)

# Parse the HTML content of the page with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all listing elements
all_link_elements = soup.select(".StyledPropertyCardDataWrapper a") 

# Python list comprehension (covered in Day 26)
all_links = [link["href"] for link in all_link_elements] 
# print(f"There are {len(all_links)} links to individual listings in total: \n")
# print(all_links)


# Create a list of all the addresses on the page using a CSS Selector
# Remove newlines \n, pipe symbols |, and whitespaces to clean up the address data
all_address_elements = soup.select(".StyledPropertyCardDataWrapper address")
all_addresses = [address.get_text().replace(" | ", " ").strip() for address in all_address_elements]
# print(f"\n After having been cleaned up, the {len(all_addresses)} addresses now look like this: \n")
# print(all_addresses)

# Create a list of all the prices on the page using a CSS Selector
# Get a clean dollar price and strip off any "+" symbols and "per month" /mo abbreviation
all_price_elements = soup.select(".PropertyCardWrapper span")
all_prices = [price.get_text().replace("/mo", "").split("+")[0] for price in all_price_elements if "$" in price.text]
# print(f"\n After having been cleaned up, the {len(all_prices)} prices now look like this: \n")
# print(all_prices)


# Google Form 
form_url = "CLIENT SIDE FORM URL GOES HERE" 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for n in range(len(all_links)):
    driver.get(form_url)
    time.sleep(2)
# Use the xpath to select the "short answer" fields in your Google Form. 
    address = driver.find_element(by=By.XPATH, 
                        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(by=By.XPATH, 
                        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(by=By.XPATH, 
                        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(by=By.XPATH, 
                        value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    
    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()
driver.quit()  # Close the browser after all entries