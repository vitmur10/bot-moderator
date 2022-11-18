import config
from aiogram import Bot, Dispatcher, executor, types
from filters import IsAdmin
from datetime import datetime, timedelta
import random

bot = Bot(token=config.Token_bot)
owm = config.owm
# logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot)


@dp.message_handler(content_types=['new_chat_members'])
async def on_user_joiner(message: types.Message):
    await message.delete()


# aктивація фільтра
dp.filters_factory.bind(IsAdmin)


# ban
@dp.message_handler(is_admin=True, commands=['ban'], commands_prefix='/')
async def ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply('Ця команда має бути відповіддю на повідомлення')
        return

    await message.bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.reply(f'Покинув нас')


# kik
@dp.message_handler(is_admin=True, content_types=["реклама", "прон", "язык"])
async def kik(message: types.Message):
        if not message.reply_to_message:
            await message.reply('Ця команда має бути відповіддю на повідомлення')
            return
        await message.bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        await message.reply(f'Покинув нас', message.reply_to_message.from_user.id)


# Mute
@dp.message_handler(is_admin=True, content_types=['text'])
async def mute(message):
    name1 = message.from_user.get_mention(as_html=True)
    muteint = {"флуд": 6,
               "накрутка": 12,
               "эпи": 48,
               "пинг": 2,
               "попрошайка": 24
               }
    if not message.reply_to_message:
        await message.reply("Ця команда має бути відповіддю на повідомлення!")
        return
    for key in muteint:
        if key == message.text:
            dt = datetime.now() + timedelta(hours=int(muteint[key]))
            timestamp: float = dt.timestamp()
            await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), timestamp)
            await message.reply(
                f' | <b>Рішення було прийняте:</b> {name1}\n | <b>Порушник:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | <b>Термін покарання:</b> {muteint[key]} годин\n | <b>Причина:</b> {message.text}',
                parse_mode='html')


@dp.message_handler(content_types=['text'])
async def filter_messages(message: types.Message):
    a = ['Відпочинь', 'Все буде добре']
    b = ['У тебе дуже гарна посмішка', 'Не думай про погане', 'Все буде добре']
    c = ['У тебе все вийде', 'Все буде добре']
    characters = {
        'z': 'Вийди отсюда розбійник🧏🧏🧏',
        'v': 'Пиздуйте нахуй отсюда йобаниє підараси👨‍🦲👨‍🦲👨‍🦲',
        'vz': 'Пиздець російській федерації⚰️⚰️⚰️',
        'Я втомився': a[random.randrange(0, len(a))],
        'Мені сумно': b[random.randrange(0, len(b))],
        'Я більше не можу': c[random.randrange(0, len(c))],
        'Я втомилася': a[random.randrange(0, len(a))]
    }
    for key in characters:
        if key == message.text:
            await message.reply(
                characters[key])
        elif set(key) == set(message.text.lower()):
            await message.reply(
                characters[key])


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Привіт')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
