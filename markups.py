from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import GROUPS


def advertisement_menu():
    advertisement_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Добавить обьявление', callback_data='channels'),
            ],
        ]
    )
    return advertisement_keyboard


def actions_with_advertisement(unique_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Изменить', callback_data=f'advertisement_change-{unique_id}'),
                InlineKeyboardButton('Удалить', callback_data='advertisement_delete'),

            ],
            [
                InlineKeyboardButton('Назад', callback_data='back-to_user_advertisements')
            ]
        ]
    )
    return keyboard


def choose_param_to_change():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Фото', callback_data='change-photo'),
                InlineKeyboardButton('Название', callback_data='change-name'),
                InlineKeyboardButton('Описание', callback_data='change-description'),
                InlineKeyboardButton('Цену', callback_data='change-price')
            ],

            [
                InlineKeyboardButton('Назад', callback_data='back-to_user_advertisement')
            ]
        ],

    )
    return keyboard


break_load_process_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отмена', callback_data='break_load_process')
        ]
    ]
)

break_changing_process_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отмена', callback_data='break_change_process')
        ]
    ]
)

back_to_main_menu = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton('Вернуться в главное меню', callback_data='back-to_advertisement_menu')
        ]
    ]
)


def set_menu_on_watching(all_ads_len, current_num):
    inline_obj = []

    if (current_num == all_ads_len - 1) and all_ads_len != 1:
        inline_obj = [InlineKeyboardButton('Предыдущее', callback_data='watch-prev')]
    elif current_num == 0:
        inline_obj = [InlineKeyboardButton('Следующее', callback_data='watch-next')]
    if 0 < current_num < all_ads_len - 1:
        inline_obj = [InlineKeyboardButton('Предыдущее', callback_data='watch-prev'),
                      InlineKeyboardButton('Следующее', callback_data='watch-next')]

    return InlineKeyboardMarkup(
        inline_keyboard=
        [
            inline_obj,
            [
                InlineKeyboardButton('Вернуться в главное меню', callback_data='back-to_advertisement_menu')
            ]
        ]
    )


# def set_menu_on_definite_watching(all_ads_len, current_num):
#     inline_obj = []
#
#     if (current_num == all_ads_len - 1) and all_ads_len != 1:
#         inline_obj = [InlineKeyboardButton('Предыдущее', callback_data='watch_definite-prev')]
#     elif current_num == 0:
#         inline_obj = [InlineKeyboardButton('Следующее', callback_data='watch_definite-next')]
#     if 0 < current_num < all_ads_len - 1:
#         inline_obj = [InlineKeyboardButton('Предыдущее', callback_data='watch_definite-prev'),
#                       InlineKeyboardButton('Следующее', callback_data='watch_definite-next')]
#
#     return InlineKeyboardMarkup(
#         inline_keyboard=
#         [
#             inline_obj,
#             [
#                 InlineKeyboardButton('Вернуться в главное меню', callback_data='back-to_advertisement_menu')
#             ]
#         ]
#     )


def on_choose_advertisement(user_advertisements):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=ad[4], callback_data=f"useradvertisement_{ad[0]}")
                for ad in user_advertisements
            ],
            [
                InlineKeyboardButton('Вернуться в главное меню', callback_data='back-to_advertisement_menu')
            ]
        ]
    )


def get_channels():
    keyb = InlineKeyboardMarkup()

    for i in GROUPS.keys():
        keyb.inline_keyboard.append(
            [InlineKeyboardButton(text=i, callback_data=f"advertisement_{GROUPS[i][0].strip()}_{GROUPS[i][1]}")]
        )
    keyb.inline_keyboard.append(
        [InlineKeyboardButton(text="Все группы", callback_data=f"advertisement_all_5900")]
    )
    return keyb


def qiwi_buy_menu(isUrl=True, url="", bill="", group_id=1):
    qiwiMenu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Проверить оплату', callback_data=f"check_{bill}_{group_id}")],
            [InlineKeyboardButton(text='Отмена', callback_data='break_load_process')]
        ]
    )
    qiwiMenu.inline_keyboard.insert(0, [InlineKeyboardButton(text='Ссылка на оплату', url=url)]) if isUrl else None
    return qiwiMenu
