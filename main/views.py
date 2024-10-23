from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Anime, lista_favoritos, Episodio
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username= request.POST['username'], password= request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                messages.error(request, 'El usuario ya existe, por favor intenta con otro nombre de usuario.')
                return render(request, 'signup.html')
        
        messages.error(request, 'Las contraseñas no coinciden')
        return render(request, 'signup.html')
    
def login_(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user = authenticate(request, username= request.POST['username'], password= request.POST['password'])
        if user is None:
            messages.error(request, 'El usuario o la contraseña son incorrectos')
            return render(request, 'login.html')
        else:
            login(request, user)
            return redirect('home')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def filter_animes(request, anime_type, template_name):
    if anime_type != 'All':
        animes = Anime.objects.filter(tipo= anime_type)
    else:
        animes = Anime.objects.all()

    gender = request.GET.get('gender')
    date = request.GET.get('date')
    status = request.GET.get('status')
    order = request.GET.get('order')

    campos_validos_para_ordenar = ['titulo_ingles', 'puntuacion', 'popularidad', 'year_of_release', 'cantidad_episodios']

    if gender and gender != 'All': 
        animes = animes.filter(generos_id__nombre = gender) #El doble guion bajo es para acceder a los campos de la tabla relacionada

    if date and date != 'All':
        try :

            año_de_estreno = int(date)
            animes = animes.filter(year_of_release = año_de_estreno)

        except:
            return render(request, '404.html', {'message': 'Ocurrió un error. Ingresó caracteres inválidos para aplicar el filtro',})
    
    if status and status != 'All':
        animes = animes.filter(estado= status)
        
    if order and order != 'All':
        
        if order.lstrip('-') in campos_validos_para_ordenar:
            animes = animes.order_by(order)
        else:
            return render(request, '404.html', {'message': 'Ocurrió un error. Ingresó caracteres inválidos para aplicar el filtro', 
            })
            
    return render(request, template_name, {'animes': animes, 'type': anime_type})


@login_required
def animes(request):
    try:
        animes = Anime.objects.all()
        return render(request, 'animes.html', {'animes': animes})
    except Exception as e:
        return HttpResponse('<h1>Ocurrió un error de tipo:</h1>, {} ,  <h1>Por favor, recarga la página.</h1>'.format(e))

@login_required
def anime_movies(request):
    try:
        return filter_animes(request, 'Película' , 'series_and_movies.html')
        
    except Exception as e:
        return HttpResponse('<h1>Ocurrió un error de tipo:</h1>, {} ,  <h1>Por favor, recarga la página.</h1>'.format(e))
    
@login_required
def anime_series(request):
    try:
        return filter_animes(request,  'Serie de TV' , 'series_and_movies.html')
    except Exception as e:
        return HttpResponse('<h1>Ocurrió un error de tipo:</h1>, {} ,  <h1>Por favor, recarga la página.</h1>'.format(e))
    
@login_required
def browse_animes(request):
    anime_type = request.GET.get('type')
    return filter_animes(request, anime_type , 'animes.html')

@login_required
def anime_detail(request, anime_id):
    anime = get_object_or_404(Anime, pk=anime_id)
    return render(request, 'anime_detail.html', {'anime': anime})

@login_required
def favorites_list(request):
    if request.method == 'GET':
        animes= Anime.objects.all()
        
        return render(request, 'create_favorites_list.html', {'animes': animes})
    
    elif request.method == 'POST':
        list_name = request.POST['name']
        list_description = request.POST['description']
        category = request.POST['category-gender']
        animes_amount = request.POST['animes-amount']

        new_list = lista_favoritos(nombre_lista= list_name, nombre_usuario= request.user, descripcion= list_description, categoria_genero= category, cantidad_animes= animes_amount)

        new_list.save()

        animes_names = request.POST.getlist('selected-animes')

        for anime_name in animes_names:
            anime = Anime.objects.get(titulo_ingles= anime_name)
            new_list.nombres_animes.add(anime)
        
        new_list.save()

        messages.success(request, 'Lista de favoritos creada con éxito')
        return redirect('create_favorites_list')

@login_required
def my_account(request):
    return render(request, 'my_account.html')

@login_required
def profile(request):
    if request.method == 'GET':
        user = request.user
        return render(request, 'profile.html', {'user': user})
    
    elif request.method == 'POST':
        user = request.user
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        messages.success(request, 'Información actualizada con éxito.')
        return redirect('my_account')
    
@login_required
def change_password(request):
    if request.method == 'GET':
        return render(request, 'change_password.html')
    elif request.method == 'POST':
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if check_password(current_password, user.password): #check_password es una función de Django que compara la contraseña actual con la contraseña del usuario
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user) #Se vuelve a autenticar al usuario para que no se cierre la sesión
                messages.success(request, 'Contraseña cambiada con éxito.')
                return redirect('my_account')
            else:
                messages.warning(request, 'La nueva contraseña y la confirmación de la contraseña no coinciden.')
                return render(request, 'change_password.html')
        else:
            messages.error(request, 'La contraseña actual es incorrecta.')
            return render(request, 'change_password.html')
        
@login_required
def manage_favorites_lists(request):
    if request.method == 'GET':
        lists = lista_favoritos.objects.filter(nombre_usuario= request.user)
        #si el queryset está vacío significa que el usuario no tiene listas de favoritos creadas por lo que retornamos un mensaje a la plantilla
        if not lists.exists():
            messages.info(request, 'No tienes listas de favoritos por el momento.')
            return render(request, 'manage_favorites_lists.html')
        else:
            return render(request, 'manage_favorites_lists.html', {'lists': lists})
    
    
    elif request.method == 'POST':
        list_id = request.POST['list_id']
        list = lista_favoritos.objects.get(pk= list_id)
        list.delete()
        messages.success(request, 'Lista eliminada con éxito.')
        return redirect('manage_favorites_lists')
    
@login_required
def list_detail(request, list_id):
    if request.method == 'GET':
        list = lista_favoritos.objects.get(pk= list_id)
        animes = list.nombres_animes.all()
        
        return render(request, 'list_detail.html', {'list': list, 'animes': animes})

@login_required
def list_edit(request, list_id):
    if request.method == 'GET':
        fav_list = lista_favoritos.objects.get(pk= list_id)
        # se obtienen los animes que están en la lista de favoritos
        animes_content_list = fav_list.nombres_animes.all()
        # se obtienen los animes que no están en la lista de favoritos
        all_animes = Anime.objects.all().exclude(id_anime__in=fav_list.nombres_animes.values_list('id_anime', flat=True))
        
        return render(request, 'list_edit.html' , {'list': fav_list , 'animes_list': animes_content_list , 'all_animes': all_animes})
    
    elif request.method == 'POST':
        fav_list = lista_favoritos.objects.get(pk= list_id)
        new_name = request.POST['name']
        new_description = request.POST['description']
        new_category = request.POST['category-gender']
        new_animes_amount = request.POST['animes-amount']
        new_animes_names = request.POST.getlist('selected-animes')

        # actualizamos los datos de la lista con los nuevos datos
        fav_list.nombre_lista = new_name
        fav_list.descripcion = new_description
        fav_list.categoria_genero = new_category
        fav_list.cantidad_animes = new_animes_amount
        #obtengo los nombres de los nuevos animes que se agregaron a la lista en el formulario
        new_animes_names = request.POST.getlist('selected-animes')
        
        
        if new_animes_names: #verifico que la lista de nuevos animes no esté vacía
            print(f" esta es lo que viene de: {new_animes_names}")
            # creo una lista vacía para almacenar los objetos Anime que se obtienen de los nombres de los animes que se agregaron a la lista
            new_animes = []
            # itero sobre los nombres de los animes que se agregaron a la lista y obtengo el objeto Anime correspondiente a cada nombre
            for anime_name in new_animes_names:
                anime = Anime.objects.get(titulo_ingles= anime_name)
                # agrego el objeto Anime a la lista de nuevos animes
                new_animes.append(anime)  
            # reemplazo los animes de la lista de favoritos por los nuevos animes
            fav_list.nombres_animes.set(new_animes)

        # guardo los cambios en la lista de favoritos
        fav_list.save()

        messages.success(request, 'Lista de favoritos editada con éxito.')
        return redirect('manage_favorites_lists')
        

    

    


    

    
    
