from aiogram import Dispatcher, Bot, types
from aiogram.utils.executor import start_webhook
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
APP_NAME = os.getenv('APP_NAME')
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)
WEBHOOK_HOST = f'https://{APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{API_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
WEBAPP_PORT = int(os.getenv('PORT'))
WEBAPP_HOST = '0.0.0.0'


url = "https://google.gik-team.com/?q="


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


@dp.inline_handler(lambda inline_query: len(inline_query.query) > 0)
async def send(inline_query):

    answer = types.InlineQueryResultArticle(id=inline_query.id, title=inline_query.query,
                                       input_message_content=types.InputTextMessageContent(message_text=(url + inline_query.query.replace(' ', '+'))))
    await bot.answer_inline_query(inline_query.id, [answer], cache_time=1)


@dp.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Привет! Я не реагирую на команды тут, '
                           'вызови меня в нужном тебе чате написав @google4youbot *свой запрос*', reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(chat_id=message.chat.id, text='Пример: @google4youbot как это работает?')

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
