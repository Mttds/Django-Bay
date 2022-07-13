from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.create_listing_view, name="add"),
    #path("categories", views.Categories.as_view(), name="categories"),
    path("categories", views.categories_view, name="categories"),
    path("categories/<int:category_id>", views.category_listings_view, name="category_listings"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("watchlist/add/<int:listing_id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist/remove/<int:listing_id>", views.watchlist_remove, name="watchlist_remove"),
    path("bid/remove/<int:bid_id>", views.bid_remove, name="bid_remove")
]
