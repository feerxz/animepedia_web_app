from django.db import models
from django.contrib.auth.models import User
from .functions import make_short_synopsis

# Create your models here.

#Un productor puede tener muchos animes asociados
class Productor(models.Model):
    class Meta:
        db_table = 'productor'
        verbose_name_plural = "Productores"
    id_productor = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=80, null=False, blank=False)
    nombre_japones= models.CharField(max_length=30, null=False, blank=False)
    descripcion= models.TextField(null=False, blank=False)
    url_sitio_web= models.CharField(max_length=80, null=False, blank=False, verbose_name= 'Link del sitio web')
    

    def __str__(self):
        return self.nombre
    
#Un anime puede tener muchos productores asociados, al igual que muchos generos y personajes
class Anime(models.Model):
    class Meta:
        db_table = 'anime'
        verbose_name = "Anime"
    id_anime = models.AutoField(primary_key=True, verbose_name="ID")
    titulo_ingles = models.CharField(max_length=80, null=False, blank=False, verbose_name="Título en inglés")
    titulo_japones = models.CharField(max_length=80, null=False, blank=False)
    synopsis = models.TextField(null=False, blank=False)
    cantidad_episodios = models.IntegerField(null=False, blank=False, verbose_name="Cantidad de episodios")
    estado = models.CharField(max_length=30, null=False, blank=False)
    puntuacion = models.FloatField(null=False, blank=False)
    popularidad = models.IntegerField(null=False, blank=False)
    tipo = models.CharField(max_length=30, null=False, blank=False)
    year_of_release = models.IntegerField(null=False, blank=False)
    imagen_url = models.CharField(max_length=80, null=False, blank=False)
    fecha_de_estreno = models.CharField(max_length=30, null=False, blank=False)
    generos_id = models.ManyToManyField('Genero', related_name='genero')
    productores_id = models.ManyToManyField('Productor', related_name='productor')
    personajes_id = models.ManyToManyField('Personaje', related_name='personaje')
    #Estos 2 campos de abajo son para saber si el anime fue creado por un usuario de la comunidad y quien es ese usuario
    create_by_community = models.BooleanField(default = False, verbose_name="Creado por la comunidad")
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='anime', verbose_name="Creado por")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.titulo_ingles
    
    # este es un "método de instancia" para obtener una versión corta de la sinopsis. Esto no se guarda en la base de datos
    def short_synopsis(self):
        return make_short_synopsis(self.synopsis)

#Un genero puede tener muchos animes asociados
class Genero(models.Model):
    class Meta:
        db_table = 'genero'
        verbose_name_plural = "Géneros"
    id_genero = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80, null=False, blank=False, verbose_name="Nombre del género")
    url_descripcion = models.TextField(null=False, blank=False, verbose_name="Link de la descripción")

    def __str__(self):
        return self.nombre
    
#Un personaje puede tener muchos animes asociados, ya que puede estar presente en varios animes
class Personaje(models.Model):
    class Meta:
        db_table = 'personaje'
    id_personaje = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=False, blank=False,verbose_name="Nombre del personaje")
    url_imagen_personaje = models.CharField(max_length=100, null=False, blank=False)
    rol = models.CharField(max_length=40, null=False, blank=False)
    
    def __str__(self):
        return self.nombre
    

#Un anime puede tener muchos episodios asociados, pero un episodio solo puede pertenecer a un anime
class Episodio(models.Model):
    class Meta:
        db_table = 'episodio'
    id_episodio = models.AutoField(primary_key=True)
    numero_episodio = models.IntegerField(null=False, blank=False)
    titulo_episodio = models.CharField(max_length=255, null=False, blank=False, verbose_name="Título del episodio")
    titulo_en_japones = models.CharField(max_length=255, null=False, blank=False)
    animes_id = models.ForeignKey('Anime', on_delete=models.CASCADE, related_name='episodio', verbose_name="Anime al que le pertenece")

    def __str__(self):
        return self.titulo_episodio

#Un usuario puede tener muchas listas de favoritos asociadas, pero una lista de favoritos solo puede pertenecer a un usuario
#Una lista de favoritos puede tener muchos animes asociados, y un anime puede estar en varias listas de favoritos
class lista_favoritos(models.Model):
    class Meta:
        db_table = 'lista_favoritos'
        verbose_name = "Lista de favoritos"
        verbose_name_plural = "Listas de favoritos"
        
    id_lista = models.AutoField(primary_key=True, verbose_name="ID")
    nombre_lista = models.CharField(max_length=40, null=False, blank=False, verbose_name="Nombre de la lista")
    nombre_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lista_favoritos', verbose_name="Usuario")
    nombres_animes = models.ManyToManyField('Anime', related_name='lista_favoritos', verbose_name="Animes que incluye")
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_de_modificacion = models.DateField(auto_now=True)
    descripcion = models.TextField(null=True, blank=True, verbose_name="Descripción de la lista")
    cantidad_animes = models.IntegerField(null=False, blank=False, verbose_name="Cantidad de animes")
    categoria_genero = models.CharField(max_length=40, null=False, blank=False, verbose_name="Categoría de género")

    def __str__(self):
        return self.nombre_lista
    


