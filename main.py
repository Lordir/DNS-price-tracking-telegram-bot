import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pickle

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# options
options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
service = Service(executable_path="D:\\Git\\DNS-price-tracking-telegram-bot\\chromedriver.exe")


def get_source_html(url):
    driver = webdriver.Chrome(service=service, options=options)
    # driver.maximize_window()

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
            while True:
                if driver.find_element(By.CLASS_NAME, "product-buy__price"):
                    time.sleep(1)
                    price = driver.find_element(By.CLASS_NAME, "product-buy__price")

                    table_names = []
                    table_prices = []
                    with open("dns_table", encoding="utf-8") as file:
                        list_position = [line for line in file]
                        for text in list_position:
                            remove_last_text = text[:-1]
                            split_text = remove_last_text.split(':')
                            table_names.append(split_text[0])
                            price_split = split_text[1].split('₽')
                            table_prices.append(int(price_split[0].replace(' ', '')))
                    if name.text in table_names:
                        index = table_names.index(name.text)
                        price_int_split = price.text.split('₽')
                        price_int = int(price_int_split[0].replace(' ', ''))
                        if price_int < table_prices[index]:
                            print(f"Цена на { name.text } уменьшилась, новая стоимость: { price.text }")
                        elif price_int > table_prices[index]:
                            print(f"Цена на {name.text} увеличилась, новая стоимость: {price.text}")
                    else:
                        with open("dns_table", "a", encoding="utf-8") as file:
                            file.write(name.text + ":" + price.text + '\n')
                    break
                else:
                    time.sleep(1)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
        driver.implicitly_wait(2)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def test():
    with open("dns_table", encoding="utf-8") as file:
        list_position = [line for line in file]
        table_names = []
        table_prices = []
        for text in list_position:
            remove_last_text = text[:-1]
            split_text = remove_last_text.split(':')
            table_names.append(split_text[0])
            price_split = split_text[1].split('₽')
            table_prices.append(int(price_split[0].replace(' ', '')))
        print(table_names)
        print(table_prices)


def main():
    get_source_html(url="https://www.dns-shop.ru/profile/wishlist/")
    # test()


if __name__ == "__main__":
    main()
