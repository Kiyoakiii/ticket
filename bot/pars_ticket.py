from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import asyncio


def get_ticket(date, departure_place, place_of_arrival, time_num) -> str:
    # Указываем путь к исполняемому файлу Chrome WebDriver
    print(f'get_ticket called with date={date}, departure_place={departure_place}, place_of_arrival={place_of_arrival}, time_num={time_num}')
    webdriver_path = "A:\Учёба\практика 2 курс\chromedriver.exe"
    print(date)

    # Создаем экземпляр Chrome WebDriver
    print("!!!!!")
    options = webdriver.ChromeOptions()
    # Запуск в безголовом режиме (без открытия окна браузера)
    #options.add_argument('--headless')
    options.page_load_strategy = 'normal'
    service = Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    # Загружаем страницу с помощью Selenium WebDriver
    url = f"https://grandtrain.ru/tickets/{departure_place}{place_of_arrival}/{date}/"
    driver.get(url)
    text = ''
    ans = 'Свободных мест нет'

    try:
        text = driver.find_element(
            By.XPATH, '/html/body/main/div[2]/form/div/div[4]/div/div[1]/div[1]/div[2]/div[4]/div[1]').text
        print(text)
        ans += text    
    except Exception:
        pass

    time.sleep(3)
    while ans == 'Свободных мест нет' or ans == '':
        driver.refresh()
        time.sleep(10)
        ans = ''
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[4]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[1]').text
            print(text)
            ans += text
            print('4:',text)
        except Exception:
            pass
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[2]').text
            print(text)     
            if text != "Выбрать места":
                ans += text
                print('5:',text)
            else:
                ans = 'Свободных мест нет'
        except Exception:
            pass
        try:
            text = driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[3]').text
            print('6:',text)
            ans += text
        except Exception:
            pass
#/html/body/main/div[2]/form/div/div[2]/div/div[1]/div/div[2]/div[4]/div[5]
#/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[1]/div[2]/div[4]/div[4]
#/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[2]/div[2]/div[4]/div[4]
        if not("Купе" in ans) and not("Плац" in ans):
            ans = ''

        print('3ans = ', ans)

        print('ans = ', ans)

    try: 
        driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[2]/div/div[1]/div/div[2]/div[4]/div[5]').click()
    except Exception:
            pass
    try: 
        driver.find_element(
                By.XPATH, f'/html/body/main/div[2]/form/div/div[2]/div/div[1]/div[{time_num}]/div[2]/div[4]/div[4]').click()
    except Exception:
            pass
#/html/body/main/div[3]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div/button
#/html/body/main/div[3]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div/button
#/html/body/main/div[3]/div/div[2]/div[1]/div[1]/div[1]/div[3]/div/div/div/button
#/html/body/main/div[3]/div/div[2]/div[1]/div[1]/div[1]/div[3]/div/div/div/div[1]/strong


#/html/body/main/div[3]/div/div[2]/div[2]/form[1]/div[1]/div[1]/div[7]/div/div[1]/div[2]/div[2]/svg/g[1]/g/g/g[8]/g/g[4]
#/html/body/main/div[3]/div/div[2]/div[2]/form[1]/div[1]/div[1]/div[7]/div/div[1]/div[2]/div[2]/svg/g[1]/g/g/g[8]/g/g[3]
#/html/body/main/div[3]/div/div[2]/div[2]/form[1]/div[1]/div[1]/div[7]/div/div[1]/div[2]/div[2]/svg/g[1]/g/g/g[8]/g/g[1]
#/html/body/main/div[3]/div/div[2]/div[2]/form[1]/div[1]/div[1]/div[7]/div/div[1]/div[2]/div[2]/svg/g[1]/g/g/g[8]/g/g[2]
    
    time.sleep(2)
    
    
    return url, ans

if __name__ == '__main__':
    date = "22.07.2023"
    departure_place = "2000000-"
    place_of_arrival = "2004001"
    ans, ans_2 =  get_ticket(date, departure_place, place_of_arrival, 1)
