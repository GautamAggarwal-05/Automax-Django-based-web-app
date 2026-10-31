from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views import View

from main.models import LikedListing, Listing
from users.forms import LocationForm, ProfileForm, UserForm
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

class ProfileView(View):

        @method_decorator(login_required,name='dispatch')
        def get(self,request):
            user_listings = Listing.objects.filter(seller=request.user.profile)
            user_liked_listings = LikedListing.objects.filter(profile = request.user.profile).all()
            user_form = UserForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)
            location_form = LocationForm(instance=request.user.profile.location)
            context = {
                'title': 'Profile',
                'user_form': user_form,
                'profile_form': profile_form,
                'location_form': location_form,
                'user_listings': user_listings,
                'user_liked_listings': user_liked_listings
            }
            return render(request, 'views/profile.html', context)

        def post(self,request):
            user_listings = Listing.objects.filter(seller=request.user.profile)
            user_liked_listings = LikedListing.objects.filter(profile = request.user.profile).all()
            user_form = UserForm(request.POST,instance=request.user)
            profile_form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
            location_form = LocationForm(request.POST,instance=request.user.profile.location)

            if user_form.is_valid() and profile_form.is_valid() and location_form.is_valid():
                user_form.save()
                profile_form.save()
                location_form.save()
                messages.success(request,f"Profile updated successfully")
            else:
                messages.error(request,f"Error updating profile. Please check the form for errors.")

            context = {
                            'title': 'Profile',
                            'user_form': user_form,
                            'profile_form': profile_form,
                            'location_form': location_form,
                            'user_liked_listings': user_liked_listings,
                            'user_listings': user_listings
                        }
            return render(request, 'views/profile.html', context)

