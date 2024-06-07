import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


async def get_time(date, departure_place, place_of_arrival) -> str:
    # Указываем путь к исполняемому файлу Chrome WebDriver
    webdriver_path = "A:\\Учёба\\практика 2 курс\\chromedriver.exe"

    # Создаем экземпляр Chrome WebDriver
    print("get_time")
    options = webdriver.ChromeOptions()
    # Запуск в безголовом режиме (без открытия окна браузера)
    options.add_argument("--headless")
    options.page_load_strategy = "normal"
    service = Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    # Загружаем страницу с помощью Selenium WebDriver
    url = f"https://grandtrain.ru/tickets/{departure_place}{place_of_arrival}/{date}/"
    driver.get(url)
    result = ""
    ans = ""
    time.sleep(2)
    try:
        text = driver.find_element(
            By.XPATH, "/html/body/main/div[2]/div/div/div/p"
        ).text
        print(text)
        return "err"
    except Exception:
        pass
    try:
        text = driver.find_element(
            By.XPATH, "/html/body/main/div[2]/div/div/section/h3"
        ).text
        print("text2")
        return "err"
    except Exception:
        pass

    #   Парсинг даты время отправления/прибытия + время в пути
    try:
        for i in range(1, 5):
            travel_time = (
                driver.find_element(
                    By.XPATH,
                    f"/html/body/main/div[3]/form/div/div[4]/div/div[1]/div[{i}]/div[2]/div[1]",
                ) .text.replace(
                    "\n",
                    " ") .split("В пути:")[1])
            result += f"{i}) Отправление:  " + driver.find_element(
                By.XPATH,
                f"/html/body/main/div[3]/form/div/div[4]/div/div[1]/div[{i}]/div[2]/div[1]/div[1]/div[1]/div[1]",
            ).text.replace(
                "\n",
                " ")
            result += (
                "\n" +
                "    Прибытие:  " +
                driver.find_element(
                    By.XPATH,
                    f"/html/body/main/div[3]/form/div/div[4]/div/div[1]/div[{i}]/div[2]/div[1]/div[1]/div[2]/div[1]",
                ).text.replace(
                    "\n",
                    " "))

            time_sum = result + "\n    В пути: " + travel_time + "\n"
            ans += time_sum
            result = ""
            print("1")
    except Exception:
        pass
    try:
        for i in range(1, 5):
            travel_time = (
                driver.find_element(
                    By.XPATH,
                    f"/html/body/main/div[3]/form/div/div[2]/div/div[1]/div[{i}]/div[2]/div[1]",
                ) .text.replace(
                    "\n",
                    " ") .split("В пути:")[1])
            result += f"{i}) Отправление:  " + driver.find_element(
                By.XPATH,
                f"/html/body/main/div[3]/form/div/div[2]/div/div[1]/div[{i}]/div[2]/div[1]/div[1]/div[1]/div[1]",
            ).text.replace(
                "\n",
                " ")
            result += (
                "\n" +
                "    Прибытие:  " +
                driver.find_element(
                    By.XPATH,
                    f"/html/body/main/div[3]/form/div/div[2]/div/div[1]/div[{i}]/div[2]/div[1]/div[1]/div[2]/div[1]",
                ).text.replace(
                    "\n",
                    " "))

            time_sum = result + "\n    В пути: " + travel_time + "\n"
            ans += time_sum
            result = ""
            print("1")
    except Exception:
        if ans == "":
            try:
                travel_time = (
                    driver.find_element(
                        By.XPATH,
                        f"/html/body/main/div[3]/form/div/div[2]/div/div[1]/div/div[2]",
                    ) .text.replace(
                        "\n",
                        " ") .split("В пути:")[1] .split("м")[0])
                result += f"{i}) Отправление:  " + driver.find_element(
                    By.XPATH,
                    f"/html/body/main/div[3]/form/div/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]",
                ).text.replace(
                    "\n",
                    " ")
                result += (
                    "\n" +
                    "    Прибытие:  " +
                    driver.find_element(
                        By.XPATH,
                        f"/html/body/main/div[3]/form/div/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/div[1]",
                    ).text.replace(
                        "\n",
                        " "))
                time_sum = result + "\n    В пути: " + travel_time + " м.\n"
                ans += time_sum
                result = ""
                print("2")
            except Exception:
                pass

    print(ans)

    return ans
