from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class Category(models.Model):
    name = models.CharField(max_length=64)
    imageUrl = models.CharField(max_length=1024, blank=True)
    createDate = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f"{self.name}"

class User(AbstractUser):
    watchlist = models.ManyToManyField('auctions.Listing', blank=True, related_name="subscribers")

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    initialPrice = models.PositiveIntegerField()
    createDate = models.DateTimeField(default=now, editable=False)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE, related_name="listings")
    imageUrl = models.CharField(max_length=1024, blank=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="mylistings")
    currentPrice = models.PositiveIntegerField()
    active = models.BooleanField(default=True) # True for Active, False for Closed
    

    def __str__(self):
        return f"{self.title}, Price: {self.currentPrice}, Owner: {self.owner}, Active: {self.active}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    price = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"<b>{self.body}</b> \nCommented by: <b>{self.user}</b>"