from django.contrib import admin

from .models import Category, Listing, User, Bid, Comment


class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("watchlist",)

# Register your models here.
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(User, UserAdmin)
admin.site.register(Bid)
admin.site.register(Comment)