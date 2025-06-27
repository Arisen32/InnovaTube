from django.shortcuts import render, redirect
from .models import User
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import logout
import requests



# Create your views here.


def registro(request): 
    if request.method == 'POST':
        name = request.POST.get('name')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        recaptcha_response = request.POST.get('g-recaptcha-response')

        if not recaptcha_response:
            return render(request, 'registro.html', {'error': 'Captcha no verificado'})

        
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if not result.get('success'):
            return render(request, 'registro.html', {'error': 'Captcha inválido'})

       
        if password != confirm_password:
            return render(request, 'registro.html', {'error': 'Las contraseñas no coinciden'})

        
        if User.objects.filter(username=username).exists():
            return render(request, 'registro.html', {'error': 'El usuario ya existe'})
        if User.objects.filter(email=email).exists():
            return render(request, 'registro.html', {'error': 'El correo ya está registrado'})



        hashed_password = make_password(password)
        
        user = User(username=username, password=hashed_password, email=email, Nombre=name, Apellido=lastname)
        user.save()
        return redirect('login')  

    # GET
    return render(request, 'registro.html')



def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # nombre de URL, no archivo HTML

    if request.method == 'POST':
        identifier = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Buscar usuario por username o email
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                return render(request, 'login.html', {'error': 'Usuario o correo no encontrado'})

        if check_password(password, user.password):
            # Iniciar sesión manualmente
            auth_login(request, user)
            return redirect('dashboard')  # redirige a nombre de URL
        else:
            return render(request, 'login.html', {'error': 'Contraseña incorrecta'})

    return render(request, 'login.html')   


def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def dashboard(request):

    return render(request, 'dashboard.html')