from django.urls import path
from .views import BaixarMusicaView, TocarMusicaView

urlpatterns = [
    path('', BaixarMusicaView.as_view(), name='buscar-musica'),
    path('tocar-musica/', TocarMusicaView.as_view(), name='tocar-musica')
]