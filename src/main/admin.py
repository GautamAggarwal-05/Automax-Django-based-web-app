from django.contrib import admin

from main.models import Listing

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Listing,ListingAdmin)