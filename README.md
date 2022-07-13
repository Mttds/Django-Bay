# Django-Bay

E-commerce with Django and Bootstrap.

## Install requirements

pip install -r requirements.txt

## Run server

python manage.py runserver 127.0.0.1:8001

## Functionalities

* Models: The application has 4 models: one for auction listings, one for auction bids, one for comments made on auction listings, and one for auction categories (all listings should have a category).

* Create Listing: Users can visit a page to create a new listing. They can specify a title for the listing, a text-based description, and what the starting bid should be. Users can also provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).

* Active Listings Page: The default route of the web application lets users view all of the currently active auction listings. For each active listing, this page displays the main information on each listing.

* Listing Page: Clicking on a listing takes the users to a page specific to that listing. On that page, users can view all the details about the listing, including the current price for the listing.

    * If the user is signed in, the user can add the item to their "Watchlist". If the item is already on the watchlist, the user can remove it.
    * If the user is signed in, the user can bid on the item if the item was posted by another user. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user should be presented with an error.
    * If the user is signed in and is the one who created the listing, the user can “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
    * If a user is signed in on a closed listing page, and the user has won that auction, the page says so.
    * Users who are signed in can add comments to the listing page. The listing displays all comments that have been made on the listing.
    * If the auction for the listing is closed users cannot post comments or place bids.
    * If a user made the last bid, he/she can remove it.

* Watchlist: Users who are signed in can visit a Watchlist page, which displays all of the listings that a user has added to their watchlist. Clicking on any of those listings takes the user to that listing's page.

* Categories: Users can visit a page that displays a list of all listing categories. Clicking on the name of any category takes the user to a page that displays all of the active listings in that category.

* Django Admin Interface: Via the Django admin interface, a site administrator is able to view, add, edit, and delete any listings, comments, and bids made on the site.
