from django.contrib import admin
from .models import Movie, WatchlistItem


# Register your models here.
admin.site.register(Movie)
admin.site.register(WatchlistItem)