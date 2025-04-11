# Generated by Django 4.2.20 on 2025-04-09 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=155)),
            ],
        ),
        migrations.CreateModel(
            name='Musica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=155)),
                ('link_mp3', models.URLField()),
                ('imagem_capa', models.URLField()),
                ('artista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicas.artista')),
            ],
        ),
    ]
