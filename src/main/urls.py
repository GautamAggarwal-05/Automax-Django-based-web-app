from django.urls import path
from .views import  edit_view, liked_listings_view, listing_view, main_view, home_view, list_view, send_email_view
urlpatterns = [
    path('', main_view ,name='main'),
    path('home/', home_view ,name='home'),
    path('list/', list_view ,name='list'),
    path('listing/<str:id>/',listing_view, name='listing'),
    path('listing/<str:id>/edit/',edit_view, name='edit'),
    path('listing/<str:id>/like/',liked_listings_view, name='like_listing'),
    path('listing/<str:id>/email/',send_email_view, name='send_email'),
   
 ]