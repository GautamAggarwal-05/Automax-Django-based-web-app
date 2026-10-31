from importlib import reload

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from main.filters import ListingsFilter
from main.form import ListingForm
from main.models import LikedListing, Listing
from users.forms import LocationForm



# Create your views here.
def main_view(request):
    return render(request, 'views/main.html',{"name":"Automax"})

@login_required
def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingsFilter(request.GET, queryset = listings)
    liked_listing_ids = set(
        LikedListing.objects.filter(
            profile=request.user.profile,
        ).values_list('listing_id', flat=True)
    )
    context = {
        "name": "Automax",
        "listings": listings,
        "listing_filter": listing_filter,
        "liked_listing_ids": liked_listing_ids
    }
    return render(request, 'views/home.html', context)

@login_required
def list_view(request):
    if request.method == 'POST':
        try:
            listing_form = ListingForm(request.POST, request.FILES)
            location_form = LocationForm(request.POST)
            if listing_form.is_valid() and location_form.is_valid():
                    listing = listing_form.save(commit=False)
                    listing_location = location_form.save()
                    listing.seller = request.user.profile
                    listing.location = listing_location
                    listing.save()
                    messages.info(request, f"{listing.model} Listing Posted successfully")
                    return redirect('home')
            else:
                raise Exception()
        except Exception as e:
            print(f"Error occured  while processing the form: {e}")
            messages.error(request, f"An error occurred while processing the form: {e}")
    elif request.method == 'GET':
        listing_form = ListingForm()
        location_form = LocationForm()
        

    return render(request,'views/list.html',{"name":"Automax","listing_form":listing_form,"location_form":location_form})


def listing_view(request,id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        return render(request,'views/listing.html',{"name":"Automax","listing":listing})
    except Exception as e:
        print(f"Error occured while fetching the listing: {e}")
        messages.error(request, f"An Invalid UUID {id} was provided or error could be :{e} ")
        return redirect('home')

def edit_view(request,id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        if request.method == 'POST':
            listing_form = ListingForm(request.POST,request.FILES,instance=listing)
            location_form = LocationForm(request.POST,instance=listing.location)
            if listing_form.is_valid() and location_form.is_valid():
                listing_form.save()
                location_form.save()
                messages.info(request, f"{listing.model} Listing Updated successfully")
                return redirect('home')
            else:
                messages.error(request, f"An error occurred while trying to edit the listing. Please check the form for errors.")
                return reload()
        else:
            listing_form = ListingForm(instance=listing)
            location_form = LocationForm(instance=listing.location)

        context = {
            "listing_form":listing_form,
            "location_form":location_form,
        }
        return render(request,'views/edit.html',context)
    except Exception as e:
        messages.error(request, f"An Invalid UUID {id} was provided or error could be :{e} ")
        return redirect('home')

@login_required
def liked_listings_view(request, id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

    listing = get_object_or_404(Listing, id=id)
    liked_listing, created = LikedListing.objects.get_or_create(
        profile=request.user.profile,
        listing=listing,
    )

    if not created:
        liked_listing.delete()

    return JsonResponse({
        'is_liked_by_user': created,
    })
