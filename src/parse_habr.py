from bs4 import BeautifulSoup
from src.parse_core import get_page, get_selenium_page
import re

def habr_parse_vac(url):
    soup = get_page(url)
    return soup

def habr_parse_job(url):
    soup = get_page(url)
    return soup