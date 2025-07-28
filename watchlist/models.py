from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)
    poster_url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class WatchlistItem(models.Model):
    STATUS_CHOICES = [
        ('TO_WATCH', 'To Watch'),
        ('WATCHING', 'Watching'),
        ('WATCHED', 'Watched'),
    ]
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TO_WATCH')
    rating = models.IntegerField(null=True, blank=True)
    is_favorite = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie.title} – ({self.status})"