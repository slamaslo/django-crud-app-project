from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    poster_url = models.URLField(blank=True)
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    overview = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    vote_average = models.FloatField(null=True, blank=True)
    vote_count = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.year})" if self.year else self.title
    
    class Meta:
        ordering = ['title']

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