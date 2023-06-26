from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import time
from auth_data import bank_password, bank_emale
import pickle

useragent = UserAgent()

# options
options = webdriver.ChromeOptions()

# user-agent
options.add_argument(f"user-agent={useragent.chrome}")

# set proxy
# options.add_argument("--proxy-server=138.128.91.65:8000")

# for ChromeDriver version 79.0.3945.16 or over
# options.add_argument("--disable-blink-features=AutomationControlled")

# headless mode
# options.add_argument("--headless")
# options.headless = True

url = "https://www.lbank.com/en-US/"
# url = "https://www.whatismybrowser.com/detect/what-is-my-user-agent/"
# url = "https://2ip.ru"

service = Service(executable_path=r"C:\drivers\chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(url=url)
    time.sleep(5)

    # print("Passing authentication...")
    # email_input = driver.find_element_by_id("index_email")
    # email_input.clear()
    # email_input.send_keys(vk_phone)
    # time.sleep(5)

    # password_input = driver.find_element_by_id("index_pass")
    # password_input.clear()
    # password_input.send_keys(vk_password)
    # time.sleep(3)
    # password_input.send_keys(Keys.ENTER)

    # # login_button = driver.find_element_by_id("index_login_button").click()
    # time.sleep(10)

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
