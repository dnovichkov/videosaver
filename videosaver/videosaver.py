from yt_dlp import YoutubeDL
from loguru import logger


def download_video_from_youtube(video_url: str) -> str:
    res_filename = ''
    with YoutubeDL() as ydl:
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


if __name__ == '__main__':

    url = 'https://www.youtube.com/watch?v=ZZv0MUVDufI'
    audio_filename = download_audio_from_youtube(url, ffmpeg_binary_location='ffmpeg.exe', preferred_quality=128)
    logger.debug(f'We save audio from {url} to {audio_filename}')

    resulted_filename = download_video_from_youtube(url)
    logger.debug(f'We save {url} to {resulted_filename}')
