from bs4 import BeautifulSoup
from selenium import webdriver

def get_soup(url):
    driver = webdriver.Firefox()
    driver.get(url)

    for i in range(30):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")

    return soup