from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    pass

class AuctionCategory(models.Model):
    class Meta:
        verbose_name_plural = "Auction categories"
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class AuctionListing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    image_url = models.URLField(blank=True)
    # if the user gets deleted his/her listings should be removed as well
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_price = models.DecimalField(decimal_places=2, max_digits=12)
    current_price = models.DecimalField(decimal_places=2, max_digits=12, blank=True)
    category = models.ForeignKey(AuctionCategory, on_delete=models.PROTECT, related_name="listings") #(e.g. Fashion, Toys, Electronics, Home, etc.).
    creation_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True) # so the admin can close the auction
    watchlisted = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="watchlist", blank=True) # many users can have the same item in the watchlist

    def save(self, *args, **kwargs):
        if not self.id:
            # at the first insertion of this listing the current price
            # should be equal to the start price because no one placed
            # any bids yet
            self.current_price = self.start_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listing', kwargs={"pk": self.pk})

class AuctionBid(models.Model):
    # all bids refer to an auction listing
    # if the listing gets removed, the bids are removed as well
    # related name to be able to do AuctionListing.bids to retrieve all bids
    # for a particular auction
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    # a user cannot be removed if there are bids in place that he/she made
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.price} bid on auction {self.auction}"

class AuctionComment(models.Model):
    # all comments refer to an auction listing
    # if the listing gets removed, the comments are removed as well
    # related name to be able to do AuctionListing.comments to retrieve all comments
    # for a particular auction
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['creation_date']

    def __str__(self):
        return f"{self.user} commented on auction {self.auction} @{self.creation_date}"
