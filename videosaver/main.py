from yt_dlp import YoutubeDL


def download_video_from_youtube(video_url):
    res_filename = ''
    with YoutubeDL() as ydl:
        info = ydl.extract_info(video_url, download=True)
        if info.get('requested_downloads'):
            res_filename = info.get('requested_downloads')[0].get('filepath')
    return res_filename


def download_audio_from_youtube(video_url, ffmpeg_binary_location=None):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    if ffmpeg_binary_location:
        ydl_opts['ffmpeg-location'] = ffmpeg_binary_location

    with YoutubeDL(ydl_opts) as ydl:
        res_filename = ''
        info = ydl.extract_info(video_url, download=True)
        # ydl.download([video_url])
        if info.get('requested_downloads'):
            res_filename = info.get('requested_downloads')[0].get('filepath')
    return res_filename


url = 'https://www.youtube.com/watch?v=ZZv0MUVDufI'
audio_filename = download_audio_from_youtube(url, 'ffmpeg.exe')
print(f'We save audio from {url} to {audio_filename}')

resulted_filename = download_video_from_youtube(url)
print(f'We save {url} to {resulted_filename}')
