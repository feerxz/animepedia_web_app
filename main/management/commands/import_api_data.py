from django.core.management.base import BaseCommand
import requests
from main.models import Anime, Genero, Productor, Personaje, Episodio

# Comando para importar datos de la API de Jikan y llenar la base de datos, no mover nada de este archivo
class Command(BaseCommand):
    help= 'Importa datos de la API de Jikan'

    def handle(self, *args, **options):
        try:    
            for page in range(1, 3):
                url = "https://api.jikan.moe/v4/anime?page={}".format(page)
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()['data']
                    for anime in data:
                        cant_episodios = anime.get('episodes')
                        if cant_episodios == None:
                            cant_episodios = 0
                        anime_ = Anime.objects.create(titulo_ingles=anime.get('title', 'Titulo desconocido'), titulo_japones=anime['title_japanese'], synopsis=anime['synopsis'], cantidad_episodios= cant_episodios, estado=anime['status'], puntuacion=anime['score'], popularidad=anime['popularity'], tipo=anime['type'], year_of_release = anime.get('aired', {}).get('prop', {}).get('from', {}).get('year'), imagen_url=anime['images']['jpg']['image_url'], fecha_de_estreno=anime['aired']['string'])

                        for genre in anime['genres']:
                            genre_, created = Genero.objects.get_or_create(nombre=genre['name'], url_descripcion=genre.get('url', 'URL desconocida'))
                            anime_.generos_id.add(genre_)

                        for producer in anime['producers']:
                            
                            producer_, created = Productor.objects.get_or_create(nombre=producer['name'])
                            if created:
                                response = requests.get(f'https://api.jikan.moe/v4/producers/{producer["mal_id"]}')
                                if response.status_code == 200:
                                    producer_data = response.json()['data']
                                    producer_.nombre_japones = 'Nombre japonés no disponible'
                                    descripcion_productor = producer_data.get('about')
                                    if descripcion_productor == None:
                                        descripcion_productor = 'Descripcion desconocida'
                                    for title in producer_data['titles']:
                                        if title['type'] == 'Japanese':
                                            producer_.nombre_japones = title['title']
                                            break
                                    producer_.descripcion = descripcion_productor
                                    producer_.url_sitio_web = producer_data['url']
                                    producer_.save()
                                    
                            anime_.productores_id.add(producer_)

                        response = requests.get(f'https://api.jikan.moe/v4/anime/{anime["mal_id"]}/characters')
                        if response.status_code == 200:
                            characters_data = response.json()['data']
                            for character in characters_data:
                                role = character.get('role', 'Rol desconocido')
                                character = character['character'] # "character" es un diccionario que contiene la informacion del personaje, por lo tanto se debe acceder a el para obtener los datos
                                character_, created = Personaje.objects.get_or_create(nombre=character.get('name','Nombre desconocido'),url_imagen_personaje= character.get('images',{}).get('jpg',{}).get('image_url', 'URL desconocida'), rol=role)
                                anime_.personajes_id.add(character_)

                        if anime['type'] != 'Movie':
                            response = requests.get(f'https://api.jikan.moe/v4/anime/{anime["mal_id"]}/episodes')
                            if response.status_code == 200:
                                episodes_data = response.json()['data']
                                for episode in episodes_data:
                                    nombre_japones_del_episodio = episode.get('title_japanese')
                                    if nombre_japones_del_episodio == None:
                                        nombre_japones_del_episodio = 'Nombre japonés no disponible'
                                    episode_, created = Episodio.objects.get_or_create(
                                    numero_episodio=episode['mal_id'], 
                                    titulo_episodio=episode['title'], 
                                    titulo_en_japones = nombre_japones_del_episodio,
                                    animes_id=anime_
                                    )
                                    
                                    episode_.save()
        except Exception as e:
            self.stdout.write(self.style.ERROR('Ocurrió un error: {}'.format(e)))  
        else:                          
            self.stdout.write(self.style.SUCCESS('Successfully imported data from Jikan API'))
                                    

                    
