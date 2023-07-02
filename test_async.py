import asyncio

# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from asyncselenium.webdriver.remote.async_webdriver import AsyncWebdriver
from asyncselenium.webdriver.support.async_wait import AsyncWebDriverWait
from asyncselenium.webdriver.support import async_expected_conditions as ec


import aiohttp

from auth_data import bank_password, bank_emale

import time

# async def check_for_class(url, class_name):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             html = await response.text()
#             soup = BeautifulSoup(html, 'lxml')
#             if soup.find(class_=class_name):
#                 return True
#             return False

options = webdriver.ChromeOptions()


def set_driver_options(options: webdriver.ChromeOptions):
    # user-agent
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.2.625 Yowser/2.5 Safari/537.36")

    # for ChromeDriver version 79.0.3945.16 or over
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    # Запустить в режиме без графического интерфейса
    # options.add_argument("--headless")
    
set_driver_options(options)

caps = DesiredCapabilities().CHROME
caps['pageLoadStrategy'] = 'eager'

service = Service(desired_capabilities=caps,
                  executable_path=r"C:\drivers\chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.lbank.com/en-US/trade/btc_usdt/"
class_name = "ant-modal-content"

try:

    # Passing authentication...
    def authentication(driver: webdriver.Chrome):
        email_input = driver.find_element(
            By.XPATH, "//input[@placeholder='Please enter your email']")
        email_input.clear()
        email_input.send_keys(bank_emale)

        password_input = driver.find_element(
            By.XPATH, "//input[@placeholder='Please enter password']")
        password_input.clear()
        password_input.send_keys(bank_password)
        password_input.send_keys(Keys.ENTER)

    # установить значение amount
    def set_amount(driver: webdriver.Chrome, arg: str, val: str):
        InputForm = driver.find_element(
            By.XPATH, f"//span[contains(text(), '{arg}')]")
        input = InputForm.find_element(By.XPATH, "./parent::div//input")
        input.clear()
        input.send_keys(val)

    # установка слайдера в максимальное значение
    def turn_trade_slider(driver: webdriver.Chrome, arg: str):
        slider = driver.find_element(
            By.XPATH, f"//div[contains(@class, '{arg}')]//div[@class='ant-slider-handle']")
        driver.execute_script("arguments[0].style.left = '100%'", slider)
        driver.execute_script(
            "arguments[0].style.transform = 'translateX(-50%)'", slider)
        driver.execute_script(
            "arguments[0].setAttribute('aria-valuenow', '100')", slider)

        # проценты
        percentage_element = slider.find_element(
            By.XPATH, "//span[contains(@style, 'left: 100%')]")
        driver.execute_script(
            "arguments[0].style.left = '100%'", percentage_element)
        driver.execute_script(
            "arguments[0].innerText = '100%'", percentage_element)

        slider_track = slider.find_element(
            By.XPATH, "//div[@class='ant-slider-track']")
        driver.execute_script(
            "arguments[0].style.width = '100%'", slider_track)

    # нажать кнопку buy/sell
    def click_trade_button(driver: webdriver.Chrome, arg: str):
        button = driver.find_element(
            By.XPATH, f"//button[contains(@class, '{arg}')]")
        driver.execute_script("arguments[0].click();", button)

    # нажать кнопку cancel/confirm Order
    # передаются два аргумента args {Cancel} / {Confirm}
    def click_trade_confirm_button(driver: webdriver.Chrome, arg: str):
        span = driver.find_element(
            By.XPATH, f"//span[contains(text(), '{arg}')]")
        button = span.find_element(By.XPATH, "./parent::button")
        driver.execute_script("arguments[0].click();", button)

    # активировать чек-бокс "Don't prompt again"
    def click_dont_prompt_again(driver: webdriver.Chrome):
        try:
            span = driver.find_element(
                By.XPATH, "//span[contains(text(), 'prompt again')]")
            check = span.find_element(By.XPATH, "./parent::div")
            driver.execute_script("arguments[0].click();", check)
        except NoSuchElementException:
            # Обработка случая, когда элемент не найден
            print("Чек-бокс не найден")

    # закрыть всплывающее диалоговое окно
    def close_dialog_window(driver: webdriver.Chrome):
        try:
            dialog = driver.find_element(
                By.CLASS_NAME, "ant-modal-content")
            closeButton = dialog.find_element(
                By.XPATH, "//button[contains(@aria-label, 'Close')]")
            driver.execute_script("arguments[0].click();", closeButton)
        except NoSuchElementException:
            # Обработка случая, когда элемент не найден
            print(
                "Всплывающее диалоговое окно не найдено")

    async def main():
        browser = await AsyncWebdriver(options=options)
        browser.maximize_window
        wait = AsyncWebDriverWait(browser, 20)
        await browser.get("https://www.lbank.com/login/")



        driver.maximize_window
        driver.get("https://www.lbank.com/login/")

        time.sleep(5)
        authentication(driver)
        time.sleep(15)
        driver.get(url)
        time.sleep(3)

        # время ожидания
        # wait = WebDriverWait(driver, 10)
        # wait_task = asyncio.create_task(wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name))))
        # await asyncio.wait_for(EC.presence_of_element_located((By.CLASS_NAME, class_name)))

        turn_trade_slider(driver, "tradeSliderGreen")
        set_amount(driver, "Buying amount", "5")
        click_trade_button(driver, "index_buy")
        while True:
            try:
                element = driver.find_element(By.CLASS_NAME, class_name)
                click_dont_prompt_again(driver)
                close_dialog_window(driver)
                # click_trade_confirm_button(driver, "Confirm")
                break  # Класс "ant-modal-content" найден, выход из цикла
            except:
                # Пауза перед повторной проверкой
                time.sleep(0.1)

        turn_trade_slider(driver, "tradeSliderRed")
        set_amount(driver, "Selling amount", "3")
        click_trade_button(driver, "index_sel")
        while True:
            try:
                element = driver.find_element(By.CLASS_NAME, class_name)
                click_dont_prompt_again(driver)
                close_dialog_window(driver)
                # click_trade_confirm_button(driver, "Confirm")
                break  # Класс "ant-modal-content" найден, выход из цикла
            except:
                # Пауза перед повторной проверкой
                time.sleep(0.1)

        # Дождаться завершения ожидания, если оно все еще выполняется
        # await wait_task

    asyncio.run(main())

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
