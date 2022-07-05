from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="▶ Bosh menyu"),
            KeyboardButton(text='💬 Biz haqimizda'),
            ],
            [
            KeyboardButton(text='🏪 Manzilimiz'),
            KeyboardButton(text='🌐 Kanalimiz'),
             ],
        ],
    resize_keyboard=True,
)

