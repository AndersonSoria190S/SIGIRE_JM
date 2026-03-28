from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Vista para la página principal
def home(request):
    return render(request, 'Registration/home.html') 

# Vista para la página de login
def login_view(request):
    return render(request, 'Registration/login.html')

@login_required
def dashboard(request):
    # Asegúrate de usar el nombre exacto de tu archivo HTML (panel.html o dashboard.html)
    return render(request, 'Registration/dashboard.html')