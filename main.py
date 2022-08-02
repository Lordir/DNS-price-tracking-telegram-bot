import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pickle
from selenium.webdriver.common.by import By

# options

options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36")


def get_source_html(url):
    driver = webdriver.Chrome(executable_path="D:\\Git\\DNS-price-tracking-telegram-bot\\chromedriver.exe",
                              options=options)

    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(5)
        for cookie in pickle.load(open("cookies", "rb")):
            driver.add_cookie(cookie)
        time.sleep(5)
        driver.refresh()
        # pickle.dump(driver.get_cookies(), open("cookies", "wb"))

        # print(driver.page_source)
        # password_input = driver.find_element(By.ID, "ir-o9898")

        time.sleep(10)

    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def main():
    get_source_html(url="https://www.dns-shop.ru/profile/wishlist/")


# "https://www.dns-shop.ru/profile/wishlist/"
if __name__ == "__main__":
    main()
