from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from fake_useragent import UserAgent
import time
from auth_data import bank_password, bank_emale
import pickle

useragent = UserAgent()

# options
options = webdriver.ChromeOptions()

# user-agent
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.2.625 Yowser/2.5 Safari/537.36")

# set proxy
# options.add_argument("--proxy-server=138.128.91.65:8000")

# for ChromeDriver version 79.0.3945.16 or over
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# headless mode
# options.add_argument("--headless")
# options.headless = True

url = "https://www.lbank.com/login/"

service = Service(executable_path=r"C:\drivers\chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.maximize_window    
    driver.get(url=url)
    time.sleep(3)

    # print("Passing authentication...")
    email_input = driver.find_element(By.XPATH, "//input[@placeholder='Please enter your email']")
    email_input.clear()
    email_input.send_keys(bank_emale)
    time.sleep(3)

    password_input = driver.find_element(By.XPATH, "//input[@placeholder='Please enter password']")
    password_input.clear()
    password_input.send_keys(bank_password)
    time.sleep(3)
    password_input.send_keys(Keys.ENTER)

    # login_button = driver.find_element_by_id("index_login_button").click()
    time.sleep(15)
    driver.get(url="https://www.lbank.com/en-US/trade/btc_usdt/")
    time.sleep(5)
    
    byButton = driver.find_element(By.XPATH, "//button[contains(@class, 'index_buy')]")
    time.sleep(5)
    byButton.click
    time.sleep(5)
    byButton.click
    time.sleep(5)
    byButton.click
    time.sleep(5)
    # ant-btn ant-btn-primary ant-btn-block index_sell
    # print("Going to the profile page...")
    # profile_page = driver.find_element_by_id("l_pr").click()
    # time.sleep(5)

    # print("Start watching the video...")
    # video_block = driver.find_element_by_class_name("VideoPreview__thumbWrap").click()
    # time.sleep(5)
    # print("Finish watching the video...")

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
