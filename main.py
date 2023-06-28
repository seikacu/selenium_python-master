from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from fake_useragent import UserAgent
import time
from auth_data import bank_password, bank_emale
import pickle

useragent = UserAgent()

# options
options = webdriver.ChromeOptions()

# user-agent
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.2.625 Yowser/2.5 Safari/537.36")


# for ChromeDriver version 79.0.3945.16 or over
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')


url = "https://www.lbank.com/login/"

caps = DesiredCapabilities().CHROME
caps['pageLoadStrategy'] = 'eager'


service = Service(desired_capabilities=caps, executable_path=r"C:\drivers\chromedriver\chromedriver.exe")
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

    time.sleep(15)
    driver.get(url="https://www.lbank.com/en-US/trade/btc_usdt/")
    time.sleep(5)

    tst_1 = driver.find_element(By.XPATH, "//span[contains(text(), 'Buying amount')]")
    tst_2 = tst_1.find_element(By.XPATH, "./parent::div//input")
    tst_2.clear()
    tst_2.send_keys("5")
        
    time.sleep(3)
    
    
    # slider_width = slider.size["width"]
    # offset = slider_width  # Смещение на всю ширину ползунка
    # action = ActionChains(driver)
    # action.drag_and_drop_by_offset(slider, offset, 0).perform()

    
    slider = driver.find_element(By.CLASS_NAME, "ant-slider-handle")
    # slider2 = driver.find_element(By.CLASS_NAME, "ant-slider-track")
    # slider_width2 =slider2.size["width"]
    slider3 = driver.find_element(By.CLASS_NAME, "ant-slider-step")
    slider_width3 = slider3.size["width"]
    
    driver.execute_script("arguments[0].style.left = '100%'", slider)
    driver.execute_script("arguments[0].setAttribute('aria-valuenow', '100')", slider)
    # slider_width = slider.size["width"]
    # offset = slider_width  # Смещение на всю ширину ползунка
    # action = ActionChains(driver)
    # action.drag_and_drop_by_offset(slider, offset, 0).perform()
    time.sleep(1)
    # slider2 = driver.find_element(By.ID("tradeSlider"))
    
    # ActionChains(driver).drag_and_drop_by_offset(slider, 50, 0).perform()
    # ActionChains(driver).click_and_hold(slider).pause(1).move_by_offset(500,0).release().perform()
    # ActionChains(driver).move_to_element(slider).pause(1).click_and_hold(slider).move_by_offset(85, 0).release().perform()
    time.sleep(4)

    
    byButton = driver.find_element(By.XPATH, "//button[contains(@class, 'index_buy')]")
    driver.execute_script("arguments[0].click();", byButton)
    time.sleep(5)
    
    
    
    
    
    tst_3 = driver.find_element(By.XPATH, "//span[contains(text(), 'Selling amount')]")
    tst_4 = tst_3.find_element(By.XPATH, "./parent::div//input")
    tst_4.clear()
    tst_4.send_keys("5")
        
    time.sleep(3)

    
    selButton = driver.find_element(By.XPATH, "//button[contains(@class, 'index_sel')]")
    driver.execute_script("arguments[0].click();", selButton)
    time.sleep(5)

    
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
