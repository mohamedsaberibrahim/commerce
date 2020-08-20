from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("create", views.create, name="create"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("closeListing/<int:listing_id>", views.closeListing, name="closeListing"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("addcoment/<int:listing_id>", views.addcoment, name="addcoment"),
    path("listing/<int:listing_id>", views.listingPage, name="listing"),
    path("mylistings", views.mylistings, name="mylistings")
]
