from django.http import JsonResponse, FileResponse
from django.views import View
import os
from django.conf import settings
from django.shortcuts import render
from yt_dlp import YoutubeDL


class BaixarMusicaView(View):
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
            'default_search': 'ytsearch5',
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

        output_dir = os.path.join(settings.MEDIA_ROOT, 'temp_audio')
        os.makedirs(output_dir, exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')

            return FileResponse(open(filename, 'rb'), content_type='audio/mpeg')

        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=500)
