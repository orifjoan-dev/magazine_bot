from typing import Union

from aiogram import types
from aiogram.types import CallbackQuery, Message
from keyboards.default.start_keyboard import menu
from keyboards.inline.menu_keyboards import (
    menu_cd,
    categories_keyboard,
    subcategories_keyboard,
    items_keyboard,
    item_keyboard,
)
from loader import dp, db



# Bosh menyu matni uchun handler
@dp.message_handler(text="▶ Bosh menyu")
async def show_menu(message: types.Message):
    # Foydalanuvchilarga barcha kategoriyalarni qaytaramiz
    await list_categories(message)

@dp.callback_query_handler(text='')

# Kategoriyalarni qaytaruvchi funksiya. Callback query yoki Message qabul qilishi ham mumkin.
# **kwargs yordamida esa boshqa parametrlarni ham qabul qiladi: (category, subcategory, item_id)
async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    # Keyboardni chaqiramiz
    markup = await categories_keyboard()

    # Agar foydalanuvchidan Message kelsa Keyboardni yuboramiz
    if isinstance(message, Message):
        await message.answer("Bo'lim tanlang", reply_markup=markup)

    # Agar foydalanuvchidan Callback kelsa Callback natbibi o'zgartiramiz
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


# Ost-kategoriyalarni qaytaruvchi funksiya
async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category)

    # Xabar matnini o'zgartiramiz va keyboardni yuboramiz
    await callback.message.edit_reply_markup(markup)


# Ost-kategoriyaga tegishli mahsulotlar ro'yxatini yuboruvchi funksiya
async def list_items(callback: CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category, subcategory)

    await callback.message.edit_text(text="Mahsulot tanlang", reply_markup=markup)


# Biror mahsulot uchun Xarid qilish tugmasini yuboruvchi funksiya
async def show_item(callback: CallbackQuery, category, subcategory, item_id):
    markup = item_keyboard(category, subcategory, item_id)

    # Mahsulot haqida ma'lumotni bazadan olamiz
    item = await db.get_product(item_id)

    if item["photo"]:
        text = f"<a href=\"{item['photo']}\">{item['product_name']}</a>\n\n"
    else:
        text = f"{item['product_name']}\n\n"
    text += f"Narxi: {item['price']}\n{item['description']}"

    await callback.message.edit_text(text=text, reply_markup=markup)


# Yuqoridagi barcha funksiyalar uchun yagona handler
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """
    :param call: Handlerga kelgan Callback query
    :param callback_data: Tugma bosilganda kelgan ma'lumotlar
    """

    # Foydalanuvchi so'ragan Level (qavat)
    current_level = callback_data.get("level")

    # Foydalanuvchi so'ragan Kategoriya
    category = callback_data.get("category")

    # Ost-kategoriya (har doim ham bo'lavermaydi)
    subcategory = callback_data.get("subcategory")

    # Mahsulot ID raqami (har doim ham bo'lavermaydi)
    item_id = int(callback_data.get("item_id"))

    # Har bir Level (qavatga) mos funksiyalarni yozib chiqamiz
    levels = {
        "0": list_categories,  # Kategoriyalarni qaytaramiz
        "1": list_subcategories,  # Ost-kategoriyalarni qaytaramiz
        "2": list_items,  # Mahsulotlarni qaytaramiz
        "3": show_item,  # Mahsulotni ko'rsatamiz
    }

    # Foydalanuvchidan kelgan Level qiymatiga mos funksiyani chaqiramiz
    current_level_function = levels[current_level]

    # Tanlangan funksiyani chaqiramiz va kerakli parametrlarni uzatamiz
    await current_level_function(
        call, category=category, subcategory=subcategory, item_id=item_id
    )

@dp.message_handler(text=['💬 Biz haqimizda'])
async def info(message: types.Message):
    photo = 'https://static.terabayt.uz/crop/s/1/728_410_RgPpMooKlpnCYuLU2d_7IeVclQdL5L-0.jpg'
    await dp.bot.send_photo(message.from_user.id,photo=photo,caption=f"<strong>Bizda eng zamonaviy va hamyonbop smartfonlar va gadjetlar</strong>\n"
                            "\n<strong>🏪 Manzil</strong> : Malika Bozori 412-do'kon"
                            "\n<strong>📞 Telefon raqam</strong> : +998 99 816 75 42"
                            "\n<strong>🌐 Kanal</strong> : https://t.me/+tdyQtfFuTHVkODgy")


@dp.message_handler(text=['🏪 Manzilimiz'])
async def location(message: types.Message):
    chat_id = message.from_user.id
    lat = 41.33873965091441
    lon = 69.27180830377654
    text = f"<strong>Malika Bozori ,Kichik Xalqa Yo'li</strong>"
    await dp.bot.send_message(chat_id=chat_id,text=text)
    await dp.bot.send_location(chat_id=chat_id,latitude=lat,longitude=lon)

@dp.message_handler(text = ['🌐 Kanalimiz'])
async def channel(message: types.Message):
    chat_id = message.from_user.id
    text = f"<strong>➡️Kanalga o'tish</strong> : https://t.me/+tdyQtfFuTHVkODgy "
    await dp.bot.send_message(chat_id=chat_id,text=text)