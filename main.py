import random
import string

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from aiogram.utils.exceptions import Unauthorized, ChatNotFound

import markups
from config import dp, bot, db, GROUPS, p2p
from states import Advertisement


@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    user_id = msg.from_user.id
    if not db.user_exists(user_id):
        await bot.send_message(user_id,
                               'Добро пожаловать в бота публикации Вашей рекламы!'
                               'Для справки можете зайти в /help', reply_markup=markups.advertisement_menu())
        db.add_user(user_id)
    else:
        await bot.send_message(user_id, 'С возвращением!', reply_markup=markups.advertisement_menu())


@dp.callback_query_handler(Text("back-to_advertisement_menu"))
async def back_to_main_menu(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, 'Вы вернулись в главное меню', reply_markup=markups.advertisement_menu())


@dp.message_handler(commands=['help'])
async def test(msg: types.Message):
    # await bot.send_message(msg.from_user.id,
    #                        'Приветствую! Это бот для выставки объявлений. Воспользуйтесь кнопками в /menu для работы '
    #                        'с ботом, помощь с конвертированием валют в /convert.\nЕсли '
    #                        'вы нашли какой-то баг, или есть какие-то вопросы на счет бота, пишите разработчику '
    #                        '@akiko233')
    await bot.send_message(-1001439847153, "test")

@dp.message_handler(commands=['creator'])
async def test(msg: types.Message):
    await bot.send_message(msg.from_user.id,
                           'Cоздатель @akiko233')


@dp.callback_query_handler(Text('break_load_process'), state=Advertisement.all_states)
async def break_load(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    await state.finish()
    await bot.send_message(call.from_user.id, 'Вы отменили загрузку объявления❌',
                           reply_markup=markups.back_to_main_menu)

    db.delete_advertisement(call.from_user.id, db.get_last_id(call.from_user.id))


@dp.callback_query_handler(Text('break_change_process'), state=Advertisement.AdvertisementActions.all_states)
async def break_load(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    await state.finish()
    await bot.send_message(call.from_user.id, 'Вы отменили процесс изменения❌'
    if state == Advertisement.AdvertisementActions.change_param
    else 'Вы отменили действие❌')


@dp.callback_query_handler(Text(startswith='channels'), state=None)
async def get_channels(call: types.CallbackQuery):
    channels = """🔥 [Поставщики](https://t.me/+zA95WH3y3SoyZTcy) \- 1999₽ 🔥

🔥[Поставщики Товарка](https://t.me/postavkatovarkabiznes) \- 999₽🔥

🔥[Товарка](https://t.me/optovikw) \- 749₽🔥

🔥[Товарочка](https://t.me/postavshchiki1) \- 499₽🔥

🔥[Grand\-Opt](https://t.me/grant_opt) \- 499₽🔥

🔥[Поставки Оптом](https://t.me/optovik5) \- 449₽🔥

🔥[Товарочка](https://t.me/postavshchiki_opt) \- 399₽🔥

🔥[Товарный бизнес](https://t.me/postavshchiki_ru) \- 199₽🔥

💥Если брать во всех, то 5900, вместо 8050₽"""

    await call.message.edit_text("Выберите канал, в который хотите отправить вашу рекламу\n\n\n" + channels,
                                 reply_markup=markups.get_channels(), parse_mode="MarkdownV2")


@dp.callback_query_handler(Text(startswith="advertisement"))
async def process_payment(call: types.CallbackQuery):
    group_id, price2 = call.data.split('_')[1:]
    price = 10

    comment = f"{call.from_user.id}_{''.join([random.choice(string.ascii_letters) for _ in range(12)])}"
    bill = p2p.bill(amount=price, lifetime=15, comment=comment)

    db.add_check(call.from_user.id, money=price, bill_id=bill.bill_id)
    await bot.send_message(call.from_user.id, f'Вам нужно отправить {price} рублей на наш счет Qiwi\n'
                                              f'Ссылка: {bill.pay_url}\n'
                                              f'Комментарий к оплате: {comment}',
                           reply_markup=markups.qiwi_buy_menu(url=bill.pay_url, bill=bill.bill_id,
                                                              group_id=group_id))

    await Advertisement.on_check_payment.set()


@dp.callback_query_handler(Text(contains='check_'), state=Advertisement.on_check_payment)
async def check_qiwi_pay(call: types.CallbackQuery, state: FSMContext):
    bill, group_id = call.data.split("_")[1:]
    info = db.get_check(bill)

    if info is not False:
        if str(p2p.check(bill_id=bill).status) == "PAID":
            await state.set_data({
                "group_id": group_id
            })

            db.delete_check(bill_id=bill)
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

            user_name = call.from_user.username
            db.set_advertisement_user(call.from_user.id, user_name)

            await bot.send_message(call.from_user.id, 'Спасибо за покупку!\n'
                                                      'Отправьте фото или видео объявления',
                                   reply_markup=markups.break_load_process_keyboard)

            await Advertisement.photo.set()
        else:
            await bot.send_message(call.from_user.id, "Вы не оплатили счет",
                                   reply_markup=markups.qiwi_buy_menu(isUrl=False, bill=bill, group_id=group_id)
                                   )
    else:
        await bot.send_message(call.from_user.id, 'Счет не найден')


@dp.message_handler(content_types=['photo', 'video'], state=Advertisement.photo)
async def set_advertisement_photo(message: types.Message):
    if message.content_type == 'photo':
        media_id = message.photo[0].file_id
    else:
        media_id = message.video.file_id

    user_id = message.from_user.id
    db.set_something(db.get_last_id(user_id), 'photo_id', media_id)

    await bot.send_message(user_id, "Теперь введите текст рекламы", reply_markup=markups.break_load_process_keyboard)
    await Advertisement.description.set()


@dp.message_handler(content_types=['text'], state=Advertisement.description)
async def set_advertisement_description(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    db.set_something(db.get_last_id(user_id), 'description', message.text)

    group_id = (await state.get_data())["group_id"]

    last_user_advertisement = db.get_user_advertisements_data(user_id)[-1]

    try:
        await bot.send_photo(user_id, last_user_advertisement[2],
                             caption=f"Ваше рекламное объявление успешно сохранено и отправлено✅\n"
                                     f"\nТекст: {last_user_advertisement[4]}",
                             reply_markup=markups.back_to_main_menu)
    except:
        await bot.send_video(user_id, last_user_advertisement[2],
                             caption=f"Ваше рекламное объявление успешно сохранено и отправлено✅\n"
                                     f"\nТекст: {last_user_advertisement[4]}",
                             reply_markup=markups.back_to_main_menu)

    if group_id == "all":
        for u_id in GROUPS:
            try:
                await bot.send_photo(u_id, last_user_advertisement[2], caption=last_user_advertisement[4],
                                     reply_markup=markups.back_to_main_menu)
            except:
                await bot.send_video(u_id, last_user_advertisement[2], caption=last_user_advertisement[4],
                                     reply_markup=markups.back_to_main_menu)
    else:
        try:
            await bot.send_photo(group_id, last_user_advertisement[2], caption=last_user_advertisement[4],
                                 reply_markup=markups.back_to_main_menu)
        except:
            await bot.send_video(group_id, last_user_advertisement[2], caption=last_user_advertisement[4],
                                 reply_markup=markups.back_to_main_menu)

    await state.finish()


@dp.message_handler(content_types=['text'])
async def get_text_from_user(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Я не понимаю, что это значит')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
