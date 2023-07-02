import cv2
import numpy as np
import requests
import time
import threading
# import cv3
# import numpy as np

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.common.action_chains import ActionChains

from auth_data import bank_password, bank_emale

options = webdriver.ChromeOptions()

def set_driver_options(options:webdriver.ChromeOptions):
    # user-agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.2.625 Yowser/2.5 Safari/537.36")

    # for ChromeDriver version 79.0.3945.16 or over
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

set_driver_options(options)

caps = DesiredCapabilities().CHROME
caps['pageLoadStrategy'] = 'eager'

service = Service(desired_capabilities=caps, executable_path=r"C:\drivers\chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# class всплывающего диалогового окна
class_name = "ant-modal-content"

try:
    
    def solve_captcha(driver:webdriver.Chrome):
        # Нахождение элементов капчи по CSS-селектору
        captcha_slider = driver.find_element(By.CSS_SELECTOR, ".yidun_slider")
        captcha_bg_img = driver.find_element(By.CSS_SELECTOR, ".yidun_bg-img")
        captcha_jigsaw = driver.find_element(By.CSS_SELECTOR, ".yidun_jigsaw")

        # Получение координат и размеров капчи
        slider_width = captcha_slider.size["width"]
        bg_img_location = captcha_bg_img.location
        bg_img_size = captcha_bg_img.size
        jigsaw_location = captcha_jigsaw.location
        
        # Получение пути к фоновому изображению капчи
        bg_img_url = captcha_bg_img.get_attribute("src")

        # Загрузка фонового изображения капчи
        response = requests.get(bg_img_url)
        with open("captcha_bg.jpg", "wb") as file:
            file.write(response.content)

        # Реализация алгоритма разгадывания капчи с использованием библиотеки OpenCV

        # Получение пути к изображению с пазлом
        jigsaw_url = captcha_jigsaw.get_attribute("src")

        # Загрузка изображения с пазлом
        response = requests.get(jigsaw_url)
        with open("captcha_jigsaw.png", "wb") as file:
            file.write(response.content)

        # Реализация алгоритма разгадывания пазла (например, с использованием библиотеки OpenCV)


        # Загрузка фонового изображения капчи и изображения с пазлом
        bg_img = cv2.imread("captcha_bg.jpg")
        jigsaw_img = cv2.imread("captcha_jigsaw.png")

        bg_img2 = cv2.imdecode("captcha_bg.jpg")
        jigsaw_img2 = cv2.imdecode("captcha_jigsaw.png")
        jigsaw_img2
        # Преобразование изображений в оттенки серого (grayscale)
        bg_gray = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)
        jigsaw_gray = cv2.cvtColor(jigsaw_img, cv2.COLOR_BGR2GRAY)

        # Инициализация детектора и описателя ключевых особенностей (например, ORB)
        detector = cv2.SIFT.create()
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).create()

        # Обнаружение ключевых особенностей и их описаний на обоих изображениях
        bg_keypoints, bg_descriptors = detector.detectAndCompute(bg_gray, None)
        jigsaw_keypoints, jigsaw_descriptors = detector.detectAndCompute(jigsaw_gray, None)

        # Сопоставление особенностей
        matches = matcher.match(bg_descriptors, jigsaw_descriptors)

        # Сортировка сопоставлений по расстоянию
        matches = sorted(matches, key=lambda x: x.distance)

        # Используем только некоторое количество наилучших сопоставлений
        num_good_matches = 10
        good_matches = matches[:num_good_matches]

        # Извлечение координат ключевых точек для хороших сопоставлений
        src_pts = np.float32([bg_keypoints[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([jigsaw_keypoints[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Вычисление матрицы преобразования (трансформации) с помощью алгоритма RANSAC
        M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)

        # Вычисление смещения пазла на фоновом изображении
        jigsaw_offset = cv2.perspectiveTransform(np.array([[0, 0], [0, jigsaw_img.shape[0]], [jigsaw_img.shape[1], jigsaw_img.shape[0]], [jigsaw_img.shape[1], 0]], dtype=np.float32).reshape(-1, 1, 2), M)
        # jigsaw_offset = cv2.perspectiveTransform(np.array([[0, 0], [0, jigsaw_img.shape[0]], [jigsaw_img.shape[1], jigsaw_img.shape[0]], [jigsaw_img.shape[1], 0]], dtype=np.float32).reshape(-1, 1, 2), M)

        # Печать смещения пазла
        print("Смещение пазла:", jigsaw_offset)


        # Расчет смещения пазла
        # jigsaw_offset = # результат алгоритма разгадывания пазла

        # Вычисление позиции для перемещения ползунка
        move_x = int(bg_img_location["x"] - jigsaw_location["x"] + jigsaw_offset)

        # Перемещение ползунка к определенной позиции
        actions = ActionChains(driver)
        actions.click_and_hold(captcha_slider).move_by_offset(move_x, 0).release().perform()

        script = '''
            var slider = arguments[0];
            var moveX = arguments[1];

            function simulateDragDrop(sourceNode, destinationNode) {
                var EVENT_TYPES = {
                    DRAG_END: 'dragend',
                    DROP: 'drop'
                }

                function createCustomEvent(type) {
                    var event = new CustomEvent("CustomEvent")
                    event.initCustomEvent(type, true, true, null)
                    event.dataTransfer = {
                        data: {
                        },
                        setData: function(type, val) {
                            this.data[type] = val
                        },
                        getData: function(type) {
                            return this.data[type]
                        }
                    }
                    return event
                }

                function dispatchEvent(node, type, event) {
                    if (node.dispatchEvent) {
                        return node.dispatchEvent(event)
                    }
                    if (node.fireEvent) {
                        return node.fireEvent("on" + type, event)
                    }
                }

                var event = createCustomEvent(EVENT_TYPES.DRAG_END)
                dispatchEvent(sourceNode, EVENT_TYPES.DRAG_END, event)
                dispatchEvent(destinationNode, EVENT_TYPES.DROP, event)
            }

            simulateDragDrop(slider, slider.offsetParent);
            slider.style.left = (slider.offsetLeft + moveX) + 'px';
        '''
        driver.execute_script(script, captcha_slider, move_x)

        # Ожидание завершения анимации и получение результата
        # Например, можно дождаться изменения класса элемента капчи после успешного прохождения
        # или проверить наличие сообщения об успешной проверке капчи

    
    # Функция для проверки наличия класса 'new_class'
    def check_dialog_class(driver:webdriver.Chrome):
        try:
            element = driver.find_element(By.CLASS_NAME, class_name)
            # Действия после появления класса class_name
            click_dont_prompt_again(driver)
            # click_trade_confirm_button(driver, "Confirm")
            # click_trade_confirm_button(driver, "Cancel")
            close_dialog_window(driver, element)
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
        email_input = driver.find_element(By.XPATH, "//input[@placeholder='Please enter your email']")
        email_input.clear()
        email_input.send_keys(bank_emale)

        password_input = driver.find_element(By.XPATH, "//input[@placeholder='Please enter password']")
        password_input.clear()
        password_input.send_keys(bank_password)
        password_input.send_keys(Keys.ENTER)    

    # установить значение amount
    def set_amount(driver:webdriver.Chrome, arg:str, val:str):
        InputForm = driver.find_element(By.XPATH, f"//span[contains(text(), '{arg}')]")
        input = InputForm.find_element(By.XPATH, "./parent::div//input")
        input.clear()
        input.send_keys(val)

    # установка слайдера в максимальное значение
    def turn_trade_slider(driver:webdriver.Chrome, arg:str): 
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

    # нажать кнопку buy/sell
    def click_trade_button(driver:webdriver.Chrome, arg:str):
        button = driver.find_element(By.XPATH, f"//button[contains(@class, '{arg}')]")
        driver.execute_script("arguments[0].click();", button)

    # нажать кнопку cancel/confirm Order
    # передаются два аргумента args {Cancel} / {Confirm}
    def click_trade_confirm_button(driver:webdriver.Chrome, arg:str):
        span = driver.find_element(By.XPATH, f"//span[contains(text(), '{arg}')]")
        button = span.find_element(By.XPATH, "./parent::button")
        driver.execute_script("arguments[0].click();", button)

    # активировать чек-бокс "Don't prompt again"
    def click_dont_prompt_again(driver:webdriver.Chrome):
        try:
            span = driver.find_element(By.XPATH, "//span[contains(text(), 'prompt again')]")
            check = span.find_element(By.XPATH, "./parent::div")
            driver.execute_script("arguments[0].click();", check)
        except NoSuchElementException:
            # Обработка случая, когда элемент не найден
            print("Чек-бокс не найден")

    # закрыть всплывающее диалоговое окно
    def close_dialog_window(driver:webdriver.Chrome, dialog):
        try:
            # dialog = driver.find_element(By.CLASS_NAME, "ant-modal-content")
            closeButton = dialog.find_element(By.XPATH, "//button[contains(@aria-label, 'Close')]")
            driver.execute_script("arguments[0].click();", closeButton)
        except NoSuchElementException:
            # Обработка случая, когда элемент не найден
            print("Всплывающее диалоговое окно не найдено")           

    driver.maximize_window
    driver.get("https://www.lbank.com/login/")
    
    time.sleep(5)
    authentication(driver)
    time.sleep(10)
    
    solve_captcha(driver)
    
    time.sleep(60)    
    driver.get("https://www.lbank.com/en-US/trade/btc_usdt/")
    time.sleep(3)


    stop_threads = False
    # Создание и запуск потока для выполнения проверки на всплывающее диалоговое окно
    thread = threading.Thread(target=check_dialog_thread, args=(lambda : stop_threads, driver, ))
    thread.start()

    turn_trade_slider(driver, "tradeSliderGreen")
    set_amount(driver, "Buying amount", "5")        
    click_trade_button(driver, "index_buy")
    
    turn_trade_slider(driver, "tradeSliderRed")
    set_amount(driver, "Selling amount", "3")
    click_trade_button(driver, "index_sel")
        
except Exception as ex:
    print(ex)
finally:
    stop_threads = True
    thread.join()
    driver.close()
    driver.quit()