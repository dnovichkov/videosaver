import logging
import os
import sys

import aiogram.utils.markdown as md
import yt_dlp
from aiogram import Bot, Dispatcher, types
from aiogram import filters
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor, exceptions
from defaultenv import env

from videosaver.videosaver import download_video_from_youtube, download_audio_from_youtube

API_TOKEN = env('API_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    video_url = State()
    file_format = State()


@dp.message_handler(commands='start')
@dp.message_handler(filters.CommandStart())
@dp.message_handler()
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """

    await Form.video_url.set()

    await message.reply("Привет. Введите ссылку на видео. Для отмены введите отмена в диалоге")


@dp.message_handler(Text(contains=['cancel', 'отмена', 'стоп'], ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)

    await state.finish()

    await message.reply('Отменено.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.video_url)
async def process_url(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['video_url'] = message.text
    # Update state and data
    await Form.next()
    await state.update_data(video_url=message.text)

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Video", "Audio", "Voice", "Отмена")

    await message.reply("Какой формат нужен? Voice - можно ускорять", reply_markup=markup)


async def process_url_invalid(message: types.Message):
    return await message.reply("Неизвестный формат ссылки, нужна ссылка на видео")


@dp.message_handler(lambda message: message.text not in ["Video", "Audio", "Voice", "Отмена"], state=Form.file_format)
async def process_format_invalid(message: types.Message):
    return await message.reply("Неизвестный формат файла. Выберите формат с клавиатуры")


def download_video_or_audio(url: str, file_format: str) -> str:
    if file_format in ['Audio', 'Voice']:
        if sys.platform == 'win32':
            return download_audio_from_youtube(url, 'videosaver/ffmpeg.exe')
        return download_audio_from_youtube(url)
    elif file_format == 'Video':
        return download_video_from_youtube(url)
    return ''


@dp.message_handler(state=Form.file_format)
async def process_file_format(message: types.Message, state: FSMContext):
    if "Отмена" in message.text:
        return await cancel_handler(message, state)

    async with state.proxy() as data:
        data['file_format'] = message.text

        # Remove keyboard
        markup = types.ReplyKeyboardRemove()

        # And send message
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Вы просили ссылку на,', md.bold(data['video_url'])),
                md.text('Формат файла:', data['file_format']),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
    file_name = None
    try:
        url = data['video_url']
        file_name = download_video_or_audio(url, data['file_format'])
        if data['file_format'] == 'Video':
            await bot.send_video(
                chat_id=message.chat.id,
                video=open(file_name, 'rb'),
                caption=f'{url} has been downloaded.'
            )
        elif data['file_format'] == 'Voice':
            await bot.send_voice(
                chat_id=message.chat.id,
                voice=open(file_name, 'rb'),
                caption=f'{url} has been downloaded.'
            )
        elif data['file_format'] == 'Audio':
            await bot.send_audio(
                chat_id=message.chat.id,
                audio=open(file_name, 'rb'),
                caption=f'{url} has been downloaded.'
            )
    except exceptions.NetworkError as ex:
        logging.error(ex)
    except yt_dlp.utils.DownloadError as ex:
        logging.error(ex)
    finally:
        if file_name:
            os.remove(file_name)

    # Finish conversation
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
