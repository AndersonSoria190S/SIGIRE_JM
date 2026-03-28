from django.shortcuts import render

# Vista para la página principal
def home(request):
    return render(request, 'registration/home.html') 

# Vista para la página de login
def login_view(request):
    return render(request, 'registration/login.html')