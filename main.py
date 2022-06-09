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
        await message.reply('Ця команда має бути відповідю на повідомлення')
        return


    await message.bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.reply(f'Покинув нас')


#kik
@dp.message_handler(is_admin=True, commands=['kik'], commands_prefix='/')
async def kik(message: types.Message):
    if not message.reply_to_message:
        await message.reply('Ця команда має бути відповідю на повідомлення')
        return

    await message.bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.reply(f'Покинув нас')


#Mute
@dp.message_handler(is_admin=True, commands=['mut'], commands_prefix='/')
async def mute(message):
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return
    try:
        muteint = int(message.text.split()[1])
        mutetype = message.text.split()[2]
        comment = " ".join(message.text.split()[3:])
    except IndexError:
        await message.reply('Не хватает аргументов!\nПример:\n`/мут 1 ч причина`')
        return
    if mutetype == "ч" or mutetype == "часов" or mutetype == "час":
        dt = datetime.now() + timedelta(hours=muteint)
        timestamp = dt.timestamp()
    elif mutetype == "м" or mutetype == "минут" or mutetype == "минуты":
        dt = datetime.now() + timedelta(minutes=muteint)
        timestamp = dt.timestamp()
    elif mutetype == "д" or mutetype == "дней" or mutetype == "день":
        dt = datetime.now() + timedelta(days=muteint)
        timestamp = dt.timestamp()
    await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False),timestamp)
    await message.reply(
        f' | <b>Решение было принято:</b> {name1}\n | <b>Нарушитель:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | <b>Срок наказания:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
        parse_mode='html')


"""@dp.message_handler()
async def filter_messages(message: types.Message):
    m2 = set(str.casefold(message.text))
    zv = ('z', 'v', 'zv', 'vz')
    for i in zv:
        if set(i) == m2:
            await message.reply(
                f'Вийди отсюда розбійник')"""


if __name__ =='__main__':
    executor.start_polling(dp, skip_updates=True)