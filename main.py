import config
#import logging
from aiogram import Bot, Dispatcher, executor, types
from filters import IsAdmin
from datetime import datetime, timedelta
import time


bot = Bot(token=config.Token_bot)

#logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot)


@dp.message_handler(content_types=['new_chat_members'])
async def on_user_joiner(message: types.Message):
    await message.delete()


#aктивація фільтра
dp.filters_factory.bind(IsAdmin)


#ban
@dp.message_handler(is_admin=True, commands=['ban'], commands_prefix='/')
async def ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply('Ця команда має бути відповіддю на повідомлення')
        return


    await message.bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.reply(f'Покинув нас')


#kik
@dp.message_handler(is_admin=True, commands=['kik'], commands_prefix='/')
async def kik(message: types.Message):
    if not message.reply_to_message:
        await message.reply('Ця команда має бути відповіддю на повідомлення')
        return

    await message.bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.reply(f'Покинув нас')


#Mute
@dp.message_handler(is_admin=True, commands=['mut'], commands_prefix='/')
async def mute(message):
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
        await message.reply("Ця команда має бути відповіддю на повідомлення!")
        return
    try:
        muteint = int(message.text.split()[1])
        mutetype = message.text.split()[2]
        comment = " ".join(message.text.split()[3:])
    except IndexError:
        await message.reply('Бракує аргументів!\nПриклад:\n`/mut 1 ч причина`')
        return
    if mutetype == "г" or mutetype == "годин" or mutetype == "година":
        dt = datetime.now() + timedelta(hours=muteint)
        timestamp = dt.timestamp()
    elif mutetype == "х" or mutetype == "хвилин" or mutetype == "хвилини":
        dt = datetime.now() + timedelta(minutes=muteint)
        timestamp = dt.timestamp()
    elif mutetype == "д" or mutetype == "днів" or mutetype == "день":
        dt = datetime.now() + timedelta(days=muteint)
        timestamp = dt.timestamp()
    await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False),timestamp)
    await message.reply(
        f' | <b>Рішення було прийняте:</b> {name1}\n | <b>Порушник:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | <b>Термін покарання:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
        parse_mode='html')


@dp.message_handler()
async def filter_messages(message: types.Message):
    m2 = set(str.casefold(message.text))
    characters = {
        'z': 'Вийди отсюда розбійник🧏🧏🧏',
        'v': 'Пиздуйте нахуй отсюда йобаниє підараси👨‍🦲👨‍🦲👨‍🦲',
        'vz': 'Пиздець російській федерації⚰️⚰️⚰️'
    }
    for key in characters:
        if set(key) == m2:
            await message.reply(
                characters[key])


if __name__ =='__main__':
    executor.start_polling(dp, skip_updates=True)