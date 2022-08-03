import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pickle

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

# options

options = webdriver.ChromeOptions()
# options.add_argument(
#     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36")


def get_source_html(url):
    driver = webdriver.Chrome(executable_path="D:\\Git\\DNS-price-tracking-telegram-bot\\chromedriver.exe",
                              options=options)

    driver.maximize_window()

    try:
        driver.get(url=url)
        driver.implicitly_wait(5)
        # load cookies
        for cookie in pickle.load(open("cookies", "rb")):
            driver.add_cookie(cookie)
        driver.implicitly_wait(1)
        driver.refresh()
        # save cookies
        # pickle.dump(driver.get_cookies(), open("cookies", "wb"))

        # print(driver.page_source)
        # password_input = driver.find_element(By.ID, "ir-o9898")
        driver.implicitly_wait(2)
        urls = driver.find_elements(By.CLASS_NAME, "catalog-product__name.ui-link.ui-link_black")
        for items in urls:
            items.send_keys(Keys.CONTROL + Keys.ENTER)
            driver.switch_to.window(driver.window_handles[1])
            name = driver.find_element(By.CLASS_NAME, "product-card-top__title")
            print(name.text)
            time.sleep(4)
            price = driver.find_element(By.CLASS_NAME, "product-buy__price")
            print(price.text)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

        # for url in range(len(driver.window_handles)-1):
        #     list_reverse = list(reversed(driver.window_handles))
        #     driver.switch_to.window(list_reverse[url])
        #     name = driver.find_element(By.CLASS_NAME, "product-card-top__title")
        #     print(name.text)
        #     if url == 0:
        #         time.sleep(10)
        #     else:
        #         time.sleep(5)
        #     price = driver.find_element(By.CLASS_NAME, "product-buy__price")
        #     print(price.text)

        # name = driver.find_element(By.CLASS_NAME, "product-card-top__title")
        # print(name.text)
        # time.sleep(15)
        #
        # price = driver.find_element(By.CLASS_NAME, "product-buy__price")
        # print(price.text)

        # price = driver.find_element(By.XPATH, "//div[@class='product-buy__price']")
        driver.implicitly_wait(2)

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
