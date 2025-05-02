from django.http import StreamingHttpResponse, JsonResponse, FileResponse
from django.views import View
import os
from django.conf import settings
from django.shortcuts import render
from yt_dlp import YoutubeDL
import subprocess


class BuscarMusicaView(View):
    def get(self, request):
        musica = request.GET.get('musica')
        lista_musicas = []

        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'extractaudio': False,
            'audioformat': 'mp3',
            'outtmpl': '%(title)s.%(ext)s',
            'default_search': 'ytsearch20',
            'skip_download': True,
            'force_generic_extractor': True
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                resultados = ydl.extract_info(musica, download=False)['entries']
                lista_musicas = []
                for item in resultados:
                    lista_musicas.append({
                        'titulo': item.get('title'),
                        'link': item.get('webpage_url'),
                        'thumb': item.get('thumbnail'),
                        'canal': item.get('uploader')
                    })


        except Exception as e:
            return render(request, 'buscar.html', {
                    'erro': str(e),
                    'musicas': []
                })
        
        return render(request, 'buscar.html', {'musicas': lista_musicas})

class TocarMusicaView(View):
    def get(self, request):
        url = request.GET.get('url')
        if not url:
            return JsonResponse({'erro': 'URL não fornecida'}, status=400)

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'noplaylist': True,
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                audio_url = info['url']
            
            ffmpeg = subprocess.Popen(
                ['ffmpeg', '-i', audio_url, '-f', 'mp3', '-'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            def stream():
                while True:
                    pedaço = ffmpeg.stdout.read(8192)
                    if not pedaço:
                        break
                    yield pedaço

            response = StreamingHttpResponse(stream(), content_type='audio/mpeg')
            return response

        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=500)
        
class PlayerMusicaView(View):
    def get(self, request):
        thumb = request.GET.get('thumb')
        titulo = request.GET.get('titulo')
        url = request.GET.get('url')

        context = {
            'thumb_musica': thumb,
            'titulo_musica': titulo,
            'url_musica': url,
        }
        return render(request, 'player.html', context)
