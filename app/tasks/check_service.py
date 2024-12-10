import httpx
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

async def process_url_check(url: str):
    """
    Проверяет доступность сайта и создает скриншот.
    """
    try:
        # Проверка HTTP-доступности
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)

        # Создание скриншота
        screenshot_path = f"screenshots/{url.replace('https://', '').replace('/', '_')}.png"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        driver.save_screenshot(screenshot_path)
        driver.quit()

        return {"status": True, "http_status": response.status_code, "screenshot_path": screenshot_path}

    except Exception as e:
        return {"status": False, "error": str(e)}
