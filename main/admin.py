from django.contrib import admin
from .models import Anime, Episodio, Genero, lista_favoritos, Personaje, Productor
# Register your models here.


class AnimeAdmin(admin.ModelAdmin):
    list_display = ('id_anime', 'titulo_ingles', 'generos_lista','tipo')
    ordering = ('id_anime',)
    search_fields = ('titulo_ingles','generos_id__nombre')
    
    # este es un método de instancia para obtener la lista de géneros separados por comas
    def generos_lista(self, obj):
        return ", ".join([genero.nombre for genero in obj.generos_id.all()])
    generos_lista.short_description = 'Géneros'

admin.site.register(Anime, AnimeAdmin)

@admin.register(lista_favoritos)
class lista_favoritosAdmin(admin.ModelAdmin):
    list_display = ('id_lista', 'nombre_lista','descripcion', 'nombre_usuario')
    ordering = ('id_lista',)
    search_fields = ('nombre_lista', 'nombre_usuario__username')
    list_editable = ('nombre_lista',)
    list_filter = ('nombre_usuario__username','fecha_creacion','nombre_lista')

@admin.register(Episodio)
class EpisodioAdmin(admin.ModelAdmin):
    list_display = ('titulo_episodio', 'numero_episodio', 'animes_id')
    ordering = ('animes_id__titulo_ingles',)
    search_fields = ('titulo_episodio', 'animes_id__titulo_ingles')

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'url_descripcion')
    ordering = ('nombre',)
    search_fields = ('nombre',)


class PersonajeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rol', 'animes_lista' )
    ordering = ('nombre',)
    search_fields = ('nombre',)

    # este es un método de instancia para obtener la lista de animes separados por comas
    def animes_lista(self, obj):
        return ", ".join([anime.titulo_ingles for anime in obj.personaje.all()])
    animes_lista.short_description = 'Anime al que pertenece'

admin.site.register(Personaje, PersonajeAdmin)

@admin.register(Productor)
class ProductorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'url_sitio_web')
    ordering = ('nombre',)
    search_fields = ('nombre',)
