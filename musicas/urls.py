from django.urls import path
from .views import BuscarMusicaView, TocarMusicaView, PlayerMusicaView

urlpatterns = [
    path('', BuscarMusicaView.as_view(), name='buscar-musica'),
    path('tocar-musica/', TocarMusicaView.as_view(), name='tocar-musica'),
    path('player/', PlayerMusicaView.as_view(), name='player'),
]