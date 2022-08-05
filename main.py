# import chromedriver_autoinstaller
from selenium import webdriver
import time
import pickle
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from token_telegram import token, chat_id

# chromedriver_autoinstaller.install()
# options
options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
service = Service(executable_path="D:\\Git\\DNS-price-tracking-telegram-bot\\chromedriver.exe")

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher(bot)

# Keyboard
button_track = KeyboardButton('track')
keyboard_bot = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_track)
# Inline keyboard
# button_track = InlineKeyboardButton(text="Проверить цены", callback_data="track")
# keyboard_bot_inline = InlineKeyboardMarkup().add(button_track)


async def get_data(url, comments):
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    try:
        if comments:
            await bot.send_message(chat_id, "Пожалуйста, подождите...")
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
        driver.implicitly_wait(2)
        urls = driver.find_elements(By.CLASS_NAME, "catalog-product__name.ui-link.ui-link_black")
        for items in urls:
            items.send_keys(Keys.CONTROL + Keys.ENTER)
            driver.switch_to.window(driver.window_handles[1])
            name = driver.find_element(By.CLASS_NAME, "product-card-top__title")
            # time.sleep(3)
            driver.implicitly_wait(20)
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
                            await bot.send_message(chat_id,
                                                   f"Цена на {name.text} уменьшилась, старая стоимость: {table_prices[index]}"
                                                   f", новая стоимость: {price.text}")
                            price_in_replace_str = list_position[index][:-1].split(':')
                            replace_line = list_position[index].replace(f"{price_in_replace_str[1]}", f"{price.text}")
                            list_position[index] = replace_line
                            with open("dns_table", "w", encoding="utf-8") as file:
                                for i in list_position:
                                    file.write(i)

                        elif price_int > table_prices[index]:
                            await bot.send_message(chat_id,
                                                   f"Цена на {name.text} увеличилась, старая стоимость: {table_prices[index]}"
                                                   f", новая стоимость: {price.text}")
                            price_in_replace_str = list_position[index][:-1].split(':')
                            replace_line = list_position[index].replace(price_in_replace_str[1], price.text)
                            list_position[index] = replace_line
                            with open("dns_table", "w", encoding="utf-8") as file:
                                for i in list_position:
                                    file.write(i)
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
        if comments:
            await bot.send_message(chat_id, "Готово")
        driver.close()
        driver.quit()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(
        f"Привет, {message.from_user.first_name}. Я отслеживаю изменение цен товаров из списка Избранное в DNS.",
        reply_markup=keyboard_bot)


# @dp.message_handler(commands=['track'])
# async def track(message: types.Message):
#     loop.create_task(get_data(url="https://www.dns-shop.ru/profile/wishlist/", comments=True))

@dp.message_handler()
async def other(message: types.Message):
    if message.text == 'track':
        loop.create_task(get_data(url="https://www.dns-shop.ru/profile/wishlist/", comments=True))

# handler for inline keyboard
# @dp.callback_query_handler(text=["track"])
# async def track(call: types.CallbackQuery):
#     if call.data == "track":
#         loop.create_task(get_data(url="https://www.dns-shop.ru/profile/wishlist/", comments=True))


async def main():
    while True:
        loop = asyncio.get_event_loop()
        loop.create_task(get_data(url="https://www.dns-shop.ru/profile/wishlist/", comments=False))
        await asyncio.sleep(3600)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    executor.start_polling(dp, skip_updates=True)
