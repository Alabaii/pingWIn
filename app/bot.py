import asyncio
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InputFile
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.site_checker import check_website_availability, take_screenshot
from app.config import settings

TOKEN =str(settings.TOKEN_TG)
dp = Dispatcher()



@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Привет! Я чат бот который проверяет доступность сайтов")


# Определяем состояния
class CheckWebsiteState(StatesGroup):
    waiting_for_url = State()

# Обработчик команды /check_website
@dp.message(Command("check_website"))
async def check_website(message: Message, state: FSMContext):
    await message.reply("Введите URL сайта для проверки:")
    await state.set_state(CheckWebsiteState.waiting_for_url)

    


@dp.message(CheckWebsiteState.waiting_for_url)
async def check_website_url(message: Message, state: FSMContext):
    print(message.text)
    url = message.text.strip()
    

    print(url)
    
    # Проверка доступности сайта
    if check_website_availability(url):
        await message.answer(f"Сайт {url} доступен!")

            # Создание скриншота сайта
        screenshot_io = take_screenshot(url)
        print(type(screenshot_io)) 


        file_path = "screenshot.png"
        with open(file_path, "wb") as f:
            f.write(screenshot_io.getvalue())
        photo = FSInputFile(file_path)
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



