import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging


logging.basicConfig(level=logging.INFO, filename='gpt-3.5-turbo.log', filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s')

bot = Bot(token='') # your telegram token
dp = Dispatcher(bot)
openai.api_key = '' # your OpenAI api key
group_id = [] # your telegram groups list ID

conversation = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

async def conversation_start(message):
    global conversation, tokens
    conversation.append({'role': 'user', 'content': message})
    for i in conversation:
        role = i.get('role')
        content = i.get('content')
        total = len(role) + len(content)
        tokens += total
    if tokens >= 3072:
        conversation = [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': message}
        ]
        tokens = int()
    return True

@dp.message_handler(content_types='text')
async def func(message: types.Message):
    if message.text[:1] == '?' and str(message.chat.id) in group_id:
        conversation_mess = await conversation_start(message.text[1:])
        if conversation_mess:
            response = await openai.ChatCompletion.acreate(
                model='gpt-3.5-turbo-0301',
                messages=conversation,
                max_tokens=1024,
                n=1,
                temperature=0.5
            )

            response_text = response['choices'][0]['message']['content']
            conversation.append({'role': 'assistant', 'content': response_text})
            await message.reply(response_text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
