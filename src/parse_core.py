import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

headers = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 6.0; rv:14.0) Gecko/20100101 '
                   'Firefox/14.0.1'),
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':
    'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding':
    'gzip, deflate',
    'Connection':
    'keep-alive',
    'DNT':
    '1'
}

def get_page(url):
    soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
    return soup

def get_selenium_page(url):
    # firefox_options = Options()
    # firefox_options.add_argument("--headless")
    # driver = webdriver.Firefox(options=firefox_options)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # driver = webdriver.Chrome(options=chrome_options)
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    # time.sleep(1)
    html = driver.page_source
    # time.sleep(1)
    driver.quit()
    return BeautifulSoup(html, 'html.parser')
