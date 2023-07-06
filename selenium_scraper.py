import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from requests_html import HTML
from selenium.webdriver.common.by import By

from request_html_test import scrape_general_information, scrape_product_details

options = Options()
options.add_argument('--headless')
PATH = r"D:\PyCharm\Scraper-One-on-One\selenium-driver\chromedriver.exe"
url = 'https://www.dominos.bg/menu/sofia-pavlovo#pizzas'
# url = 'https://www.dominos.bg/menu/sofia-pavlovo#pasta'
driver = webdriver.Chrome()

driver.get(url)
time.sleep(5)

html_data = driver.page_source


def pizza_range():
    a = set(range(0, 31))
    a.difference_update({0, 1, 2, 4, 25})
    return a


def pasta_range():
    return range(1, 6)


for x in pizza_range():
    try:
        element = driver.find_element(By.XPATH, f'//*[@id="1"]/div[2]/div/div[{x}]/div[2]')  # pizza
        # element = driver.find_element(By.XPATH, f'//*[@id="3"]/div[2]/div/div[{x}]/div[2]') # pasta
        element.click()
        time.sleep(2)

        html_data = driver.page_source
        scrape_product_details(HTML(html=html_data))
        driver.back()
        time.sleep(1)
    except :
        pass

# scrape_product_details(HTML(html=driver.page_source))
# scrape_general_information(r_html)
