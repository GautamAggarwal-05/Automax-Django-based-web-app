from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views import View
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request=request,data = request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,f'Your are logged in as {username}')
                return redirect('home')
            else:
                messages.error(request,f'Invalid username or password')
        else:
            messages.error(request,f'Invalid username or password')
    elif request.method == 'GET':
        login_form = AuthenticationForm()
    return render(request, 'views/login.html', {'title': 'Login', 'login_form': login_form})

def logout_view(request):
    logout(request)
    messages.success(request,f'You have been logged out')
    return redirect('home')


class RegisterView(View):
    def get(self,request):
        register_form = UserCreationForm()
        return render(request, 'views/register.html', {'title': 'Register', 'register_form': register_form})

    def post(self,request):
        register_form = UserCreationForm(data=request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()
            login(request,user)
            messages.success(request,f"User {user.username} registered successfully")
            return redirect('home')
        else:
            messages.error(request,f"Unsuccessful registration. Invalid information.")
        return render(request, 'views/register.html', {'title': 'Register', 'register_form': register_form})