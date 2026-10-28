from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
def main_view(request):
    return render(request, 'views/main.html',{"name":"Automax"})

@login_required
def home_view(request):
    return render(request, 'views/home.html',{"name":"Automax"})