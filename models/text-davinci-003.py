import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging


logging.basicConfig(level=logging.INFO, filename='text-davinci-003.log', filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s')

bot = Bot(token='') # your telegram token
dp = Dispatcher(bot)
openai.api_key = '' # your OpenAI api key
group_id = [] # your telegram groups list ID

@dp.message_handler(content_types='text')
async def func(message: types.Message):
    if message.text[:1] == '?' and str(message.chat.id) in group_id:
        response = await openai.ChatCompletion.acreate(
            model='text-davinci-003',
            messages=conversation,
            max_tokens=1024,
            n=1,
            temperature=0.5
        )

        response_text = response['choices'][0]['message']['content']
        await message.reply(response_text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
