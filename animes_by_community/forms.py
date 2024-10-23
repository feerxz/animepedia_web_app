from django import forms

from main.models import Anime, Genero, Productor, Personaje, Episodio 

class AnimeForm(forms.ModelForm):
    ESTADO_CHOICES = [
        ('En emisión', 'En emisión'),
        ('Finalizado', 'Finalizado'),
    ]
    TIPO_CHOICES = [('Serie de TV', 'Serie de TV'), ('Película', 'Película'), ('OVA', 'OVA')]
    genero = forms.ModelMultipleChoiceField(queryset=Genero.objects.all(), widget = forms.CheckboxSelectMultiple, label='Género(s):')

    productores = forms.ModelMultipleChoiceField(queryset=Productor.objects.all(), widget = forms.CheckboxSelectMultiple, label='Productor(es):')

    #puntuacion = forms.FloatField(required=False, label='Puntuación: (Ejemplo: 8.5)')
    #popularidad = forms.IntegerField(required=False, label='Popularidad. (Ejemplo: 1000)')
    estado = forms.ChoiceField(choices=ESTADO_CHOICES, widget= forms.Select(attrs={'class': 'form-select'}), label='Estado:')

    tipo = forms.ChoiceField(choices=TIPO_CHOICES, widget= forms.Select(attrs={'class': 'form-select'}), label='Tipo:')

    class Meta:
        model = Anime
        fields = ['titulo_ingles',  'titulo_japones', 'synopsis', 'cantidad_episodios', 'estado', 'genero', 'productores', 'year_of_release','tipo', 'fecha_de_estreno', 'imagen_url', 'puntuacion', 'popularidad']
        labels = {
            'titulo_ingles': 'Título en inglés: (Ejemplo: Dragon Ball Z)',
            'titulo_japones': 'Título en japonés: (Ejemplo: ドラゴンボール)',
            'synopsis': 'Sinopsis:',
            'cantidad_episodios': 'Cantidad de episodios: (Ejemplo: 12)',
            'year_of_release': 'Año de lanzamiento: (Ejemplo: 1999)',
            'imagen_url': 'Link de la imagen: (Ejemplo: https://www.imagen.com/imagen.jpg)',
            'fecha_de_estreno': 'Período que estuvo en emisión: (Ejemplo: Octubre 10, 2001 a ...?)',
        }

class PersonajeForm(forms.ModelForm):
    class Meta:
        model = Personaje
        fields = ['nombre', 'url_imagen_personaje', 'rol']
        labels = {
            'nombre': 'Nombre del personaje: (Ejemplo: Goku)',
            'rol': 'Rol del personaje: (Ejemplo: Principal/Secundario)',
            'url_imagen_personaje': 'Link de una imagen del personaje: (Ejemplo: https://www.imagen.com/imagen.jpg)',
        }
        
    

class EpisodioForm(forms.ModelForm): 
    class Meta:
        model = Episodio
        fields = ['numero_episodio', 'titulo_episodio', 'titulo_en_japones']
        labels = {'numero_episodio': 'Número del episodio: (Ejemplo: 1)',
                   'titulo_episodio': 'Título del episodio: (Ejemplo: El inicio)', 'titulo_en_japones': 'Título en japonés: (Ejemplo: はじめ)'
        }

class ProductorForm(forms.ModelForm):
    class Meta:
        model = Productor
        fields = ['nombre', 'nombre_japones', 'descripcion', 'url_sitio_web']
        labels = {
            'nombre': 'Nombre del productor: (Ejemplo: Toei Animation)',
            'nombre_japones': 'Nombre en japonés: (Ejemplo: 東映アニメーション)',
            'descripcion': 'Descripción: (Ejemplo: Toei Animation es una empresa de animación japonesa...)',
            'url_sitio_web': 'Link del sitio web: (Ejemplo: https://www.toei-animation.com/)',
        }
    
    # Este método es para que los campos no sean requeridos debido a que es opcional si el usuario ingresa un nuevo productor para el anime, aquí sobre-escribimos el método __init__ de la clase padre
    def __init__(self, *args, **kwargs):
        super(ProductorForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].required = False
        self.fields['nombre_japones'].required = False
        self.fields['descripcion'].required = False
        self.fields['url_sitio_web'].required = False
        