import asyncio
from fastapi import FastAPI

from contextlib import asynccontextmanager


from app.bot import start_bot, shutdown_event  # Импортируйте ваш Telegram-бот

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Выполняем действия перед запуском приложения
    loop = asyncio.get_event_loop()
    bot_task = loop.create_task(start_bot())
    
    try:
        yield
    finally:
        # Выполняем действия при завершении приложения
        shutdown_event.set()  # Сигнализируем о завершении
        bot_task.cancel()
        try:
            await bot_task
        except asyncio.CancelledError:
            pass  # Ожидаем завершения задачи бота

app = FastAPI(lifespan=lifespan)



