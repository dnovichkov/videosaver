from yt_dlp import YoutubeDL


def download_video_from_youtube(video_url):
    res_filename = ''
    with YoutubeDL() as ydl:
        info = ydl.extract_info(video_url, download=True)
        if info.get('requested_downloads'):
            res_filename = info.get('requested_downloads')[0].get('filepath')
    return res_filename


url = 'https://www.youtube.com/watch?v=ZZv0MUVDufI'
resulted_filename = download_video_from_youtube(url)
print(f'We save {url} to {resulted_filename}')
