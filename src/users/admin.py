from django.contrib import admin
from .models import Profile
from .models import Location
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    pass

class LocationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Location,LocationAdmin)