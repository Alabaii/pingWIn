import asyncio
import signal
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InputFile
from app.site_checker import check_website_availability, take_screenshot

TOKEN ='7834198872:AAFdjoRNdxdWvfzOSQKDqeSg01V0oevDFSc'
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer("По кнопке ниже вы можете оформить заказ!")

@dp.message(Command("check_website"))
async def check_website(message: Message):
    url = message.text.split(" ")[1] if len(message.text.split(" ")) > 1 else ""
    
    if not url:
        await message.answer("Привет! Я бот для проверки доступности сайтов")
        return
    
    
    # Проверка доступности сайта
    if check_website_availability(url):
        await message.answer(f"Сайт {url} доступен!")

        # Создание скриншота сайта
        screenshot_io = take_screenshot(url)
        print(type(screenshot_io)) 
        screenshot_io.seek(0)
        
        
        

        
        photo = InputFile(file=screenshot_io, filename="screenshot.png")
        # Отправка скриншота в Telegram
        await message.answer_photo(photo=photo, caption=f"Скриншот сайта: {url}")
    else:
        await message.answer(f"Сайт {url} недоступен.")



async def start_bot() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.bot = bot
    await dp.start_polling(bot)

# Обработчик завершения для Telegram бота
shutdown_event = asyncio.Event()



async def shutdown():
    await shutdown_event.wait()
    dp.bot.session.close()



