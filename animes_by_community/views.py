from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AnimeForm, PersonajeForm, EpisodioForm, ProductorForm
from main.models import Genero, Personaje, Anime, Episodio, Productor
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required
def create_anime(request):
    genero_choices = {
        'Action': 'Acción',
        'Award Winning': 'Premiados',
        'Adventure': 'Aventura',
        'Romance': 'Romance',
        'Comedy': 'Comedia',
        'Drama': 'Drama',
        'Mystery': 'Misterio',
        'Supernatural': 'Sobrenatural',
        'Slice of Life': 'Reflexión de vida',
        'Suspense': 'Suspenso',
        'Ecchi': '+18',
        'Gourmet': 'Cocina',
        'Avant Garde': 'Heavy Metal',
        'Fantasy': 'Fantasía',
        'Horror': 'Terror',
        'Sci-Fi': 'Ciencia Ficción',
        'Sports': 'Deportes',
    }
    if request.method == 'GET':
        form = AnimeForm()
        personajeform = PersonajeForm(prefix='personaje')
        episodioform = EpisodioForm()
        productorform = ProductorForm(prefix='productor')
        return render(request, 'animes_by_community/create_anime.html', {'form': form, 'personaje_form': personajeform, 'episodio_form': episodioform, 'productor_form': productorform, 'genero_choices': genero_choices}) 

    elif request.method == 'POST':
        anime_form = AnimeForm(request.POST)
        if anime_form.is_valid():
            print(f"Datos del formulario: {anime_form.cleaned_data}")
            titulo_ingles = anime_form.cleaned_data.get('titulo_ingles')
            if Anime.objects.filter(titulo_ingles=titulo_ingles).exists():
                return HttpResponse('Este anime ya existe')
            else: 
                anime = anime_form.save(commit=False)
                anime.create_by_community = True
                anime.create_by = request.user
                anime.save()
                
                # El bloque de código a continuación verifica si el usuario me ingresó un nuevo productor (que no se encuentra en la base de datos) y lo agrega a la base de datos en caso de que no exista.
                if 'productor-nombre' in request.POST and request.POST.getlist('productor-nombre')[0] != '':
                    for i in range(len(request.POST.getlist('productor-nombre'))):
                        productor, created = Productor.objects.get_or_create(
                            nombre=request.POST.getlist('productor-nombre')[i], 
                            defaults={
                                'nombre_japones': request.POST.getlist('productor-nombre_japones')[i],
                                'descripcion': request.POST.getlist('productor-descripcion')[i],
                                'url_sitio_web': request.POST.getlist('productor-url_sitio_web')[i],
                            }
                        )
                        anime.productores_id.add(productor)

                generos = request.POST.getlist('genero')
                for genero_id in generos:
                    genero = Genero.objects.get(id_genero=genero_id)
                    anime.generos_id.add(genero)

                productores = request.POST.getlist('productores')
                for productor_id in productores:
                    productor = Productor.objects.get(id_productor=productor_id)
                    anime.productores_id.add(productor)
                    
                for i in range(len(request.POST.getlist('personaje-nombre'))):
                    personaje, created = Personaje.objects.get_or_create(
                        nombre=request.POST.getlist('personaje-nombre')[i], 
                        url_imagen_personaje=request.POST.getlist('personaje-url_imagen_personaje')[i], 
                        rol=request.POST.getlist('personaje-rol')[i]
                    )
                    anime.personajes_id.add(personaje)
                for i in range(len(request.POST.getlist('numero_episodio'))):
                    episodio, created = Episodio.objects.get_or_create(
                        numero_episodio=request.POST.getlist('numero_episodio')[i],
                        titulo_episodio=request.POST.getlist('titulo_episodio')[i],
                        titulo_en_japones=request.POST.getlist('titulo_en_japones')[i],
                        animes_id=anime

                    )
                    anime.episodio.add(episodio)
                anime.save()
                
            messages.success(request, 'Anime creado con éxito.')
            return redirect('animes_by_community:manage_animes_by_me')
        
        else:
            print(f"Errores del formulario: {anime_form.errors}")
            return HttpResponse('Formulario inválido')
        
@login_required
def show_animes_by_community(request):
    animes = Anime.objects.filter(create_by_community=True)
    return render(request, 'animes_by_community/animes_by_community.html', {'animes': animes})

@login_required
def manage_animes_by_me(request):
    if request.method == 'GET':
        animes = Anime.objects.filter(create_by=request.user)

        if not animes.exists():
            messages.info(request, 'No has aportado animes por el momento.')
            return render(request,'animes_by_community/manage_animes_by_me.html')
        else:
            return render(request, 'animes_by_community/manage_animes_by_me.html', {'animes': animes})
    
    elif request.method == 'POST':
        anime_id = request.POST.get('anime_id')
        anime = Anime.objects.get(id_anime=anime_id)
        anime.delete()
        messages.success(request, 'Anime eliminado con éxito.')
        return redirect('animes_by_community:manage_animes_by_me')
        


