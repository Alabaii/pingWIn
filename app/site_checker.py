import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from io import BytesIO
# from app.config import Settings

# Функция для проверки доступности сайта
def check_website_availability(url: str) -> bool:
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200  # Если код ответа 200, сайт доступен
    except requests.exceptions.RequestException:
        return False

# Функция для создания скриншота сайта
def take_screenshot(url: str) -> BytesIO:
    # Настройка опций для работы с Selenium (без открытия окна браузера)
    options = Options()
    options.headless = True  # Запускать браузер в фоновом режиме

    # Запуск Chrome WebDriver
    driver = webdriver.Chrome(options=options)

    # Открытие страницы
    driver.get(url)

    # Делаем скриншот и сохраняем его в байтовый поток
    screenshot = driver.get_screenshot_as_png()

    # Закрываем браузер
    driver.quit()

    return BytesIO(screenshot)
