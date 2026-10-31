from django import forms

from users.widgets import CustomPhotoImageFieldWidget
from .models import Location, Profile, User
from localflavor.us.forms import USStateSelect, USZipCodeField

class UserForm(forms.ModelForm):
    username = forms.CharField(disabled=True)  # making the username field read-only
    class Meta:
        model = User
        fields = {'username', 'first_name','last_name'}

class ProfileForm(forms.ModelForm):
    photo = forms.ImageField(widget=CustomPhotoImageFieldWidget)
    bio = forms.TextInput()
    class Meta:
        model = Profile
        fields = {'photo', 'bio', 'phone_number'}

class LocationForm(forms.ModelForm):
    address_1 = forms.CharField(required=True)
    zip_code = USZipCodeField(required=True)
    class Meta:
        model = Location
        fields = {'address_1','address_2', 'city', 'state', 'zip_code'}

