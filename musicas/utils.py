from rest_framework.decorators import api_view
from rest_framework.response import Response
import urllib.parse
from yt_dlp import YoutubeDL
import requests

@api_view(['GET'])
def buscar_audio_youtube(request):
    query = request.GET.get('q')
    if not query:
        return Response({'erro': 'Query não fornecida'}, status=400)

    search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    response = requests.get(search_url)

    video_id = None
    for line in response.text.split('"'):
        if '/watch?v=' in line:
            video_id = line.split('watch?v=')[-1]
            break

    if not video_id:
        return Response({'erro': 'Vídeo não encontrado'}, status=404)

    url = f'https://www.youtube.com/watch?v={video_id}'

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'skip_download': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        audio_url = info_dict['url']
        titulo = info_dict.get('title', '')
        artista = info_dict.get('uploader', '')

    return Response({
        'titulo': titulo,
        'artista': artista,
        'stream_url': audio_url,
    })