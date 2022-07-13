from django.contrib import admin
from .models import AuctionCategory, AuctionListing, AuctionBid, AuctionComment

# Register your models here.
admin.site.register(AuctionCategory)
admin.site.register(AuctionListing)
admin.site.register(AuctionBid)
admin.site.register(AuctionComment)
