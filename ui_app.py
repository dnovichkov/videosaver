import sys
from nicegui import ui as _ui, app

from loguru import logger

from videosaver.videosaver import download_video_or_audio


def run_download(ui, radio, input_text):

    ui.label('Запустили загрузку')
    logger.debug('Run!')
    ui.label(f'Вы выбрали {radio.value}')
    ui.label(f'Адрес видео {input_text.value}')
    logger.debug(radio.value)
    logger.debug(input_text.value)

    file_name = download_video_or_audio(input_text.value, radio.value)
    logger.debug(f'{file_name=}')
    ui.link('Файл готов', file_name)


def show_ui(ui):
    ui.label('Примитивная скачивалка видео')
    radio1 = ui.radio(["Video", "Audio", "Voice - высокое качество", "Voice - среднее качество",
                       "Voice - низкое качество"], value="Audio").props('inline')

    input_text = ui.input(label='Ссылка на видео', placeholder='Введите ссылку')

    ui.button('Поехали!', on_click=lambda: run_download(ui, radio1, input_text))

    # TODO: Change directory for files
    app.add_static_files('/static', '/')
    ui.run()


if __name__ in {"__main__", "__mp_main__"}:
    logger.remove()
    logger.add(sys.stdout, level="TRACE")
    show_ui(_ui)
