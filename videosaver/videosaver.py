import sys

from yt_dlp import YoutubeDL
from loguru import logger


def download_video_from_youtube(video_url: str) -> str:
    res_filename = ''
    ydl_opts = {
        "format": "best[filesize<=50M][ext=mp4] / w[ext=mp4]",
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        if info.get('requested_downloads'):
            res_filename = info.get('requested_downloads')[0].get('filepath')
    logger.debug(f'{video_url} saved to {res_filename}')
    return res_filename


def download_audio_from_youtube(video_url: str, ffmpeg_binary_location=None, preferred_quality=128) -> str:
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': str(preferred_quality),
        }],
    }
    if ffmpeg_binary_location:
        filepath = ffmpeg_binary_location
        ydl_opts['ffmpeg_location'] = filepath

    with YoutubeDL(ydl_opts) as ydl:
        res_filename = ''
        info = ydl.extract_info(video_url, download=True)
        # ydl.download([video_url])
        if info.get('requested_downloads'):
            res_filename = info.get('requested_downloads')[0].get('filepath')
    logger.debug(f'{video_url} saved to {res_filename}')
    return res_filename


def download_video_or_audio(url: str, file_format: str) -> str:
    if file_format in ["Audio", "Voice - высокое качество", "Voice - среднее качество", "Voice - низкое качество"]:
        quality_names = {"Audio": 128,
                         "Voice - высокое качество": 128,
                         "Voice - среднее качество": 64,
                         "Voice - низкое качество": 32,
                         }
        # Default quality is 128
        quality = quality_names.get(file_format, 128)
        logger.info(f'Скачиваем {url} в формате {file_format} - {quality}')
        if sys.platform == 'win32':
            return download_audio_from_youtube(url, 'videosaver/ffmpeg.exe', preferred_quality=quality)
        return download_audio_from_youtube(url, preferred_quality=quality)
    if file_format == 'Video':
        return download_video_from_youtube(url)
    return ''


if __name__ == '__main__':

    _url = 'https://www.youtube.com/watch?v=ZZv0MUVDufI'
    audio_filename = download_audio_from_youtube(_url, ffmpeg_binary_location='ffmpeg.exe', preferred_quality=128)
    logger.debug(f'We save audio from {_url} to {audio_filename}')

    resulted_filename = download_video_from_youtube(_url)
    logger.debug(f'We save {_url} to {resulted_filename}')

