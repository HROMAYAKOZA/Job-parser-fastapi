from bs4 import BeautifulSoup
from src.parse_core import get_page, get_selenium_page
import re

def avito_parse_vac(url):
    soup = get_page(url)
    return soup

def avito_parse_job(url):
    soup = get_page(url)
    return soup