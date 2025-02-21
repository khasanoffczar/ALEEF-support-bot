from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import sqlite3
import random

# Твой TOKEN от @BotFather
TOKEN = "YOUR_BOT_TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Подключение к базе данных (SQLite)
conn = sqlite3.connect("barbershop.db")
cursor = conn.cursor()

# Создаем таблицу для записей клиентов
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        phone TEXT,
        service TEXT,
        barber TEXT,
        date TEXT,
        time TEXT
    )
""")
conn.commit()

# Клавиатура главного меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("💇 Онлайн-запись"), KeyboardButton("ℹ️ О нас"))

# Клавиатура выбора услуги
service_menu = ReplyKeyboardMarkup(resize_keyboard=True)
service_menu.add("Стрижка", "Бритье", "Оформление бороды", "Назад")

# Клавиатура выбора барбера
barber_menu = ReplyKeyboardMarkup(resize_keyboard=True)
barber_menu.add("Мастер 1", "Мастер 2", "Назад")

# Функция для ежедневных постов с юмором
jokes = [
    "💈 Барбер спрашивает клиента: - Как вас подстричь? - Бесплатно можно? - Можно, но в этот раз без головы!",
    "👨‍🦲 Клиент: - Мне, пожалуйста, как на фото! Барбер смотрит на фото... а там лысый 😂",
    "👨‍🔬 Клиент барберу: - Можно без машинки? Только ножницами? - Конечно, но будет дольше и дороже... - Ладно, тогда давайте ножницами... Барбер достает маникюрные ножницы 🤣"
]

# Узбекские шутки
jokes_uz = [
    "💈 Барбер mijozdan so'raydi: - Qanday qilib soch qirqamiz? - Bepul bo'ladimi? - Bo'ladi, faqat bu safar boshsiz 😂",
    "👨‍🦲 Mijoz: - Menga sur'atdagidek qiling! Barber qaraydi... va suratda kal odam 😆",
    "👨‍🔬 Mijoz: - Mashinasiz faqat qaychi bilan bo'ladimi? - Albatta, lekin qimmatroq... - Mayli, bo'lsa bo'ldi... Barber manikyur qaychisini chiqaradi 🤣"
]

async def send_daily_joke():
    joke = random.choice(jokes + jokes_uz)
    await bot.send_message(YOUR_CHAT_ID, joke)

scheduler = AsyncIOScheduler()
scheduler.add_job(send_daily_joke, "interval", days=1)
scheduler.start()

# Старт
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("👋 Добро пожаловать в барбершоп ALEEF! Чем могу помочь?", reply_markup=main_menu)

# Онлайн-запись
@dp.message_handler(lambda message: message.text == "💇 Онлайн-запись")
async def book_appointment(message: types.Message):
    await message.answer("Выберите услугу:", reply_markup=service_menu)

# Информация о барбершопе
@dp.message_handler(lambda message: message.text == "ℹ️ О нас")
async def about_us(message: types.Message):
    await message.answer("📍 Барбершоп ALEEF\n📌 Адрес: Kagan, Dustlik Street, 150\n📞 Телефон: +998XX XXX-XX-XX\n💬 Оставьте отзыв: [Aleef на Яндекс Картах](https://yandex.com/maps/org/232960558355?si=4khwyj6u3u6uhmrjue45pn9m2w)")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
