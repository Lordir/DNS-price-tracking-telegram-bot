import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time


def get_source_html(url):
    driver = webdriver.Chrome(executable_path="D:\Git\DNS-price-tracking-telegram-bot\chromedriver.exe")

    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(3)

    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def main():
    get_source_html(url="https://www.dns-shop.ru/profile/wishlist/")


if __name__ == "__main__":
    main()
