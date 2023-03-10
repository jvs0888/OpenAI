import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging


logging.basicConfig(level=logging.INFO, filename='dall-e-2.log', filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s')

bot = Bot(token='') # your telegram token
dp = Dispatcher(bot)
openai.api_key = '' # your OpenAI api key
group_id = [] # your telegram groups list ID

@dp.message_handler(content_types='text')
async def func(message: types.Message):
    if message.text[:1] == '!' and str(message.chat.id) in group_id:
        try:
            response = await openai.Image.acreate(
                prompt=message.text,
                n=1,
                size='512x512'
            )

            image_url = response['data'][0]['url']
            image = types.InputFile.from_url(image_url)

            await bot.send_photo(
                chat_id=message.chat.id,
                photo=image,
            )

        except Exception as e:
            print(e)
            await message.reply("Sorry, something went wrong. Please try again.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
