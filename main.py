import time
import threading

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from auth_data import bank_password, bank_emale

options = webdriver.ChromeOptions()

def set_driver_options(options:webdriver.ChromeOptions):
    # user-agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.2.625 Yowser/2.5 Safari/537.36")

    # for ChromeDriver version 79.0.3945.16 or over
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    
    # Запустить в режиме без графического интерфейса
    # options.add_argument("--headless")

set_driver_options(options)

caps = DesiredCapabilities().CHROME
caps['pageLoadStrategy'] = 'eager'

service = Service(desired_capabilities=caps, executable_path=r"C:\drivers\chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# class всплывающего диалогового окна
class_name = "ant-modal-content"
stop_threads = False

try:
    
    # Функция для проверки наличия класса 'new_class'
    def check_dialog_class(driver:webdriver.Chrome):
        try:
            element = driver.find_element(By.CLASS_NAME, class_name)
            # Действия после появления класса class_name
            click_dont_prompt_again(driver)
            # click_trade_confirm_button(driver, "Confirm")
            # click_trade_confirm_button(driver, "Cancel")
            close_dialog_window(driver, element)
            click_i_see(driver, element)
        except:
            pass
        
    # Функция для выполнения проверки в отдельном потоке
    def check_dialog_thread(stop, driver:webdriver.Chrome):
        while True:
            check_dialog_class(driver)
            if stop():
                break    
    
    # Passing authentication...
    def authentication(driver:webdriver.Chrome):
        try:
            email_input = driver.find_element(By.XPATH, "//input[@placeholder='Please enter your email']")
            email_input.clear()
            email_input.send_keys(bank_emale)

            password_input = driver.find_element(By.XPATH, "//input[@placeholder='Please enter password']")
            password_input.clear()
            password_input.send_keys(bank_password)
            
            password_input.send_keys(Keys.ENTER)    
        except NoSuchElementException:
            print("Поля аутентификации не найдены")
            pass

    # нажать Market
    def click_order(driver:webdriver.Chrome, arg:str):
        try:
            order = driver.find_element(By.XPATH, f"//div[contains(text(), '{arg}')]")
            driver.execute_script("arguments[0].click();", order)
        except NoSuchElementException:
            print(f"Кнопка {arg} не найдена")
            pass
       

    # установить значение amount
    def set_amount(driver:webdriver.Chrome, arg:str, val:str):
        try:
            input = driver.find_element(By.XPATH, f"//input[@placeholder='{arg}']")                        
            input.clear()
            input.send_keys(val)
        except NoSuchElementException:
            print(f"Поле для ввода {arg} не найдено")
            pass

    # установка слайдера в максимальное значение
    def turn_trade_slider(driver:webdriver.Chrome, arg:str):
        try:
            slider = driver.find_element(By.XPATH, f"//div[contains(@class, '{arg}')]//div[@class='ant-slider-handle']")        
            driver.execute_script("arguments[0].style.left = '100%'", slider)
            driver.execute_script("arguments[0].style.transform = 'translateX(-50%)'", slider)
            driver.execute_script("arguments[0].setAttribute('aria-valuenow', '100')", slider)

            # проценты
            percentage_element = slider.find_element(By.XPATH, "//span[contains(@style, 'left: 100%')]")
            driver.execute_script("arguments[0].style.left = '100%'", percentage_element)
            driver.execute_script("arguments[0].innerText = '100%'", percentage_element)
            
            slider_track = slider.find_element(By.XPATH, "//div[@class='ant-slider-track']")
            driver.execute_script("arguments[0].style.width = '100%'", slider_track)
        except NoSuchElementException:
            print(f"Не могу сдвинуть слайдер {arg}")
            pass

    # нажать кнопку buy/sell
    def click_trade_button(driver:webdriver.Chrome, arg:str):
        try:
            button = driver.find_element(By.XPATH, f"//button[contains(@class, '{arg}')]")
            driver.execute_script("arguments[0].click();", button)
        except NoSuchElementException:
            print(f"Не могу сдвинуть слайдер {arg}")
            pass

    # нажать кнопку cancel/confirm Order
    # передаются два аргумента args {Cancel} / {Confirm}
    def click_trade_confirm_button(driver:webdriver.Chrome, arg:str):
        try:
            span = driver.find_element(By.XPATH, f"//span[contains(text(), '{arg}')]")
            button = span.find_element(By.XPATH, "./parent::button")
            driver.execute_script("arguments[0].click();", button)
        except NoSuchElementException:
            print(f"Кнопка {arg} не найдена")
            pass

    # активировать чек-бокс "Don't prompt again"
    def click_dont_prompt_again(driver:webdriver.Chrome):
        try:
            span = driver.find_element(By.XPATH, "//span[contains(text(), 'prompt again')]")
            check = span.find_element(By.XPATH, "./parent::div")
            driver.execute_script("arguments[0].click();", check)
        except NoSuchElementException:
            print("Чек-бокс не найден")
            pass

    # закрыть всплывающее диалоговое окно
    def close_dialog_window(driver:webdriver.Chrome, dialog):
        try:
            closeButton = dialog.find_element(By.XPATH, "//button[contains(@aria-label, 'Close')]")
            driver.execute_script("arguments[0].click();", closeButton)
        except NoSuchElementException:
            print("Кнопка Close не найдена")    
            pass       

    # Нажать кнопку I see
    def click_i_see(driver:webdriver.Chrome, dialog):
        try:
            span = dialog.find_element(By.XPATH, "//span[contains(text(), 'I see')]")
            button = span.find_element(By.XPATH, "./parent::button")
            driver.execute_script("arguments[0].click();", button)
        except NoSuchElementException:
            print("Кнопка I see не найдена")     
            pass      

    driver.maximize_window
    driver.get("https://www.lbank.com/login/")
    
    time.sleep(5)
    authentication(driver)
    time.sleep(15)
    driver.get("https://www.lbank.com/en-US/trade/btc_usdt/")
    time.sleep(3)

    stop_threads = False
    # Создание и запуск потока для выполнения проверки на всплывающее диалоговое окно
    thread = threading.Thread(target=check_dialog_thread, args=(lambda : stop_threads, driver, ))
    thread.start()

    click_order(driver, "Market")
    time.sleep(2)        
    turn_trade_slider(driver, "tradeSliderGreen")
    time.sleep(2)        
    set_amount(driver, "Enter buying amount", "5")        
    time.sleep(2)        
    click_trade_button(driver, "index_buy")
    
    time.sleep(2)        
    turn_trade_slider(driver, "tradeSliderRed")
    time.sleep(2)        
    set_amount(driver, "Enter selling amount", "3")
    time.sleep(2)        
    click_trade_button(driver, "index_sel")

except Exception as ex:
    print(ex)
finally:
    stop_threads = True
    thread.join()
    driver.close()
    driver.quit()