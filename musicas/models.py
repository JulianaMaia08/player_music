from django.db import models

class ArtistaModel(models.Model):

    nome = models.CharField(max_length=155)

    def __str__(self):
        return self.nome
    
class MusicaModel(models.Model):
    titulo = models.CharField(max_length=155)
    artista = models.ForeignKey(ArtistaModel, on_delete=models.CASCADE)
    link_mp3 = models.URLField()
    imagem_capa = models.URLField()

    def __str__(self):
        return f"{self.titulo} - {self.artista.nome}"



