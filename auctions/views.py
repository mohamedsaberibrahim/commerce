from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import Category, Listing, User, Bid, Comment

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'description', 'initialPrice', 'category', 'imageUrl')
        
        labels = {
            'title': 'Listing Title', 
            'description': 'Listing Description', 
            'initialPrice': 'Price in $', 
            'category': 'Category', 
            'imageUrl': 'Image URL'
        }

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        
        labels = {
            'body': ''
        }

class CreateBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('price',)
        
        labels = {
            'price': ''
        }

def index(request):
    return render(request, "auctions/index.html",{
        "listings" : Listing.objects.exclude(active=False).all(),
        "pageTitle" : "Active Listings"
    })

@login_required(login_url="/login")
def watchlist(request, listing_id):
    current_user = request.user
    
    if request.method == "POST":
        if request.POST["_method"] == "PUT":
            current_user.watchlist.add(Listing.objects.get(id=listing_id))
        elif request.POST["_method"] == "DELETE":
            current_user.watchlist.remove(Listing.objects.get(id=listing_id))
    return render(request, "auctions/index.html",{
        "listings" : current_user.watchlist.all(),
        "pageTitle" : "Watchlist"
    })
    
@login_required(login_url="/login")
def mylistings(request):
    current_user = request.user
    return render(request, "auctions/index.html",{
        "listings" : current_user.mylistings.all(),
        "pageTitle" : "My Listings"
    })

def categories(request):
    return render(request, "auctions/categories.html",{
        "categories" : Category.objects.all()
    })

def category(request, category_id):
    category = Category.objects.get(id=category_id)
    return render(request, "auctions/index.html",{
        "listings" : category.listings.exclude(active=False).all(),
        "pageTitle" : category.name
    })

@login_required(login_url="/login")
def create(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            price =  form.cleaned_data["initialPrice"]
            listing = Listing(title=form.cleaned_data["title"], description=form.cleaned_data["description"],
            initialPrice=price, category=form.cleaned_data["category"],
            imageUrl=form.cleaned_data["imageUrl"], currentPrice=price, owner=request.user)
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=(listing.pk,)))
    return render(request, "auctions/create.html",{
        "form": CreateListingForm()
    })

@login_required(login_url="/login")
def addcoment(request, listing_id):
    if request.method == "POST":
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            comment = Comment(user=request.user, body=form.cleaned_data["body"], listing=Listing.objects.get(pk=listing_id))
            comment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required(login_url="/login")
def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        form = CreateBidForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data['price']
            if listing.bids.all():
                if price <= listing.currentPrice:
                    form.add_error('price', forms.ValidationError(
                                ('Your bid must be more than the last bid: %(price)s'),
                                code='invalid',
                                params={'price': listing.currentPrice},
                            ))
                    return render(request, "auctions/bid.html",{
                    "listing" : listing,
                    "bids" : listing.bids.all(),
                    "bidForm" : form
                })
            else:
                if price < listing.initialPrice:
                    form.add_error('price', forms.ValidationError(
                                ('Your bid must be at least as large as the starting bid: %(price)s'),
                                code='invalid',
                                params={'price': listing.initialPrice},
                            ))
                    return render(request, "auctions/bid.html",{
                    "listing" : listing,
                    "bids" : listing.bids.all(),
                    "bidForm" : form
                })
            newbid = Bid(user=request.user, price=price, listing=listing)
            newbid.save()
            listing.currentPrice = price
            listing.save()
    return render(request, "auctions/bid.html",{
        "listing" : listing,
        "bids" : listing.bids.all(),
        "bidForm" : CreateBidForm(initial={'price' : listing.currentPrice})
    })

@login_required(login_url="/login")
def closeListing(requset, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def listingPage(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    # Bids total if listing is active, Get the winner if closed
    if listing.active is True:
        bidsCount = listing.bids.all().count()
        if bidsCount == 0:
            bidsMessage = "No bids so far!"
        if bidsCount > 0:
            bidsMessage = f"{bidsCount} bid(s) so far!"
    else:
        bidsCount = listing.bids.all().count()
        if bidsCount == 0:
            bidsMessage = "No one won this listing!"
        if bidsCount > 0:
            bidWinner= listing.bids.last()
            if bidWinner.user == request.user:
                bidsMessage = f"You won it for {bidWinner.price}!"
            else:
                bidsMessage = f"{bidWinner.user} won it for {bidWinner.price}!"
    return render(request, "auctions/listing.html",{
        "listing" : listing,
        "comments" : listing.comments.all(),
        "bidsComment" : bidsMessage,
        "commentForm" : CreateCommentForm(),
        "subscribers" : listing.subscribers.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
