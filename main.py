from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from fake_useragent import UserAgent
import time
from auth_data import bank_password, bank_emale

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
    driver.get(url)
    time.sleep(5)
    
    # print("Passing authentication...")
    email_input = driver.find_element(By.XPATH, "//input[@placeholder='Please enter your email']")
    email_input.clear()
    email_input.send_keys(bank_emale)

    password_input = driver.find_element(By.XPATH, "//input[@placeholder='Please enter password']")
    password_input.clear()
    password_input.send_keys(bank_password)
    password_input.send_keys(Keys.ENTER)    
    
    time.sleep(15)
    
    driver.get("https://www.lbank.com/en-US/trade/btc_usdt/")
    
    time.sleep(5)

    buyInputForm = driver.find_element(By.XPATH, "//span[contains(text(), 'Buying amount')]")
    inputBuy = buyInputForm.find_element(By.XPATH, "./parent::div//input")
    inputBuy.clear()
    inputBuy.send_keys("5")
        
    tradeSliderGreen = driver.find_element(By.XPATH, "//div[contains(@class, 'tradeSliderGreen')]")
    buySlider = tradeSliderGreen.find_element(By.CLASS_NAME, "ant-slider-handle")
    
    driver.execute_script("arguments[0].style.left = '100%'", buySlider)
    driver.execute_script("arguments[0].setAttribute('aria-valuenow', '100')", buySlider)
        
    byButton = driver.find_element(By.XPATH, "//button[contains(@class, 'index_buy')]")
    driver.execute_script("arguments[0].click();", byButton)
    
    # всплывающее окно и его закрытие
    dialog = driver.find_element(By.CLASS_NAME, "ant-modal-content")
    closeButton = dialog.find_element(By.XPATH, "//button[contains(@aria-label, 'Close')]")
    driver.execute_script("arguments[0].click();", closeButton)

    # time.sleep(2)
    
    sellInputForm = driver.find_element(By.XPATH, "//span[contains(text(), 'Selling amount')]")
    inputSell = sellInputForm.find_element(By.XPATH, "./parent::div//input")
    inputSell.clear()
    inputSell.send_keys("3")
        
    tradeSliderRed = driver.find_element(By.XPATH, "//div[contains(@class, 'tradeSliderRed')]")
    sellSlider = tradeSliderRed.find_element(By.CLASS_NAME, "ant-slider-handle")

    driver.execute_script("arguments[0].style.left = '100%'", sellSlider)
    driver.execute_script("arguments[0].setAttribute('aria-valuenow', '100')", sellSlider)

    selButton = driver.find_element(By.XPATH, "//button[contains(@class, 'index_sel')]")
    driver.execute_script("arguments[0].click();", selButton)
    
    # time.sleep(2)
    
    # всплывающее окно и его закрытие
    dialog = driver.find_element(By.CLASS_NAME, "ant-modal-content")
    closeButton = dialog.find_element(By.XPATH, "//button[contains(@aria-label, 'Close')]")
    driver.execute_script("arguments[0].click();", closeButton)

    time.sleep(5)
    
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()