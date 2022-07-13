from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from decimal import Decimal

from .models import User, AuctionListing, AuctionCategory, AuctionComment, AuctionBid
from .forms import CreateListingForm, BidForm, CommentForm

class Index(ListView):
    model = AuctionListing
    template_name = "auctions/index.html"
    # ListView class handles the pagination by default
    # with this attribute set. It will give access to paginator and page_obj 
    # in the context accessible fromt the templating engine
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add watchlist to the context
        if self.request.user.is_authenticated:
            context['watchlist'] = self.request.user.watchlist.all()
        return context

class Categories(ListView):
    model = AuctionCategory
    template_name = "auctions/categories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add watchlist to the context
        if self.request.user.is_authenticated:
            context['watchlist'] = self.request.user.watchlist.all()
        return context

def categories_view(request):
    categories = AuctionCategory.objects.all()
    listings_dict = {}
    for category in categories:
        listings_dict[category.name] = ', '.join([l.title for l in category.listings.all()])

    return render(request, "auctions/categories.html", {
        "auctioncategory_list": categories,
        "listings_dict": listings_dict,
        "watchlist": request.user.watchlist.all() if request.user.is_authenticated else None
    })

def watchlist_view(request):
    # If no user is signed in, return to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    watchlist = request.user.watchlist.all()
    print(watchlist)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def watchlist_add(request, listing_id):
    if request.user.is_authenticated:
        try:
            auction = AuctionListing.objects.get(id=listing_id)
            auction.watchlisted.add(request.user)
        except ObjectDoesNotExist as e:
            pass

    return redirect(listing_view, listing_id=listing_id)

def watchlist_remove(request, listing_id):
    if request.user.is_authenticated:
        try:
            auction = AuctionListing.objects.get(id=listing_id)
            if request.user in auction.watchlisted.all():
                auction.watchlisted.remove(request.user)
        except ObjectDoesNotExist as e:
            pass

    return redirect(listing_view, listing_id=listing_id)

def bid_remove(request, bid_id):
    if request.user.is_authenticated:
        try:
            bid = AuctionBid.objects.get(id=bid_id)
            if request.user == bid.user:
                bid.delete()
                auction = bid.auction
                auction_bids = auction.bids.all()
                if auction_bids.count() != 0:
                    new_last_bid = auction_bids.order_by("-price")[0]
                    auction.current_price = new_last_bid.price
                else:
                    auction.current_price = auction.start_price
                auction.save()

        except ObjectDoesNotExist as e:
            return HttpResponseRedirect(reverse("index"))

    return redirect(listing_view, listing_id=bid.auction.id)

def category_listings_view(request, category_id):
    try:
        category = AuctionCategory.objects.get(id=category_id)
    except ObjectDoesNotExist as e:
        return render(request, "auctions/category_listings.html", {
            "error": "The category was not found",
            "category": "N/A"
        })

    listings = category.listings.all()
    return render(request, "auctions/category_listings.html", {
        "listings": listings,
        "category": category.name,
        "watchlist": request.user.watchlist.all() if request.user.is_authenticated else None
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

def listing_view(request, listing_id):
    try:
        auction = AuctionListing.objects.get(id=listing_id)
    except ObjectDoesNotExist as e:
        return render(request, "auctions/listing.html", {
            "error": "The auction listing was not found"
        })

    bids = auction.bids.all()
    comments = auction.comments.all()
    watchlist = request.user.watchlist.all()

    last_bid = None
    try:
        last_bid = bids.order_by("-price")[0]
    except Exception:
        pass

    if request.method == "POST":
        # If no user is signed in, return to login page
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        if 'bid' in request.POST:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                print(bids.count())
                if (auction.current_price > Decimal(request.POST.get('price')) and bids.count() == 0) \
                    or (auction.current_price >= Decimal(request.POST.get('price')) and bids.count() != 0):
                    # bid cannot be lower than the current price if there are bids. It can be the same
                    # if there are no bids yet
                    return render(request, "auctions/listing.html", {
                        'listing': auction,
                        'bids': bids,
                        'bid_form': BidForm(initial = {'price': auction.current_price + 1 if bids.count() != 0 else auction.current_price}),
                        'comment_form': CommentForm(),
                        'comments': comments,
                        'last_bid': last_bid,
                        'watchlist': watchlist,
                        'error': f"Bid of {request.POST.get('price')} cannot be lower than the current price"
                    })

                # if the last bid was made by the current user it doesn't make sense to let them bid again
                if (last_bid is not None and last_bid.user == request.user):
                    return render(request, "auctions/listing.html", {
                        'listing': auction,
                        'bids': bids,
                        'bid_form': BidForm(initial = {'price': auction.current_price + 1 if bids.count() != 0 else auction.current_price}),
                        'comment_form': CommentForm(),
                        'comments': comments,
                        'last_bid': last_bid,
                        'watchlist': watchlist,
                        'error': f"Your bid of {last_bid.price} is the last bid. You cannot bid again."
                    })

                obj = bid_form.save(commit=False)
                obj.auction = auction
                obj.user = request.user
                auction.current_price = obj.price # update the current price for the auction
                auction.save()
                obj.save()
                return redirect(listing_view, listing_id=auction.id)
        
        if 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                content = comment_form['content'].value()
                obj = AuctionComment(content=content, user=request.user, auction=auction)
                obj.save()
                return redirect(listing_view, listing_id=auction.id)

        if 'close' in request.POST:
            if auction.user != request.user:
                return render(request, "auctions/listing.html", {
                    'listing': auction,
                    'bids': bids,
                    'bid_form': BidForm(initial = {'price': auction.current_price + 1 if bids.count() != 0 else auction.current_price}),
                    'comment_form': CommentForm(),
                    'comments': comments,
                    'last_bid': last_bid,
                    'watchlist': watchlist,
                    'error': f"Only the user that posted the listing can close the auction for this listing!"
                })
            else:
                auction.is_active = False
                auction.save()
                return redirect(listing_view, listing_id=auction.id)

    if request.method == "GET":
        # 1 dollar more than the current price if there is at least one bid
        min_bid = auction.current_price + 1 if bids.count() != 0 else auction.current_price
        bid_form = BidForm(initial = {'price': min_bid})
        comment_form = CommentForm()

    return render(request, "auctions/listing.html", {
        'listing': auction,
        'bids': bids,
        'bid_form': bid_form,
        'last_bid': last_bid,
        'comment_form': comment_form,
        'watchlist': watchlist,
        'comments': comments,
    })

def create_listing_view(request):
    # If no user is signed in, return to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    watchlist = request.user.watchlist.all()

    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user # add the user creating the listing before saving
            obj.save()
            # redirect the user to the created entry
            return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': obj.id}))
        else:
            return render(request, "auctions/add.html", {
                'form': CreateListingForm(),
                'watchlist': watchlist
            })

    if request.method == "GET":
        return render(request, "auctions/add.html", {
            'form': CreateListingForm(),
            'watchlist': watchlist
        })

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
