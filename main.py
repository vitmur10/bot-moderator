import config
import logging
from aiogram import Bot, Dispatcher, executor, types
from filters import IsAdmin
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.Token_bot)

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

    #await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)
    await message.reply_to_message.reply('Користувач забанений')


@dp.message_handler()
async def filter_messages(message: types.Message):
    if 'погане слово' in message.text:
        await message.delete()

if __name__ =='__main__':
    executor.start_polling(dp, skip_updates=True)