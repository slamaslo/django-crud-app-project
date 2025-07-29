from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from .forms import UserForm
from .models import WatchlistItem, Movie

class Home(LoginView):
    template_name = 'home.html' 

# Create your views here.
def landing(request):
    return render(request, 'landing.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('watchlist_home')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserForm()
    return render(request, 'registration/signup.html', {'form': form, 'error_message': error_message})

@login_required
def watchlist_home(request):
    items = WatchlistItem.objects.filter(user=request.user)
    return render(request, 'watchlist/watchlist_home.html', {'items': items})

# @login_required
def movie_list(request):
    movies = Movie.objects.all()
    if request.user.is_authenticated:
        watchlisted_ids = WatchlistItem.objects.filter(user=request.user).values_list('movie_id', flat=True)
    else:
        watchlisted_ids = []

    return render(request, 'watchlist/movie_list.html', {'movies': movies, 'watchlisted_ids': watchlisted_ids})

@login_required
def add_to_watchlist(request, movie_id):
    if request.method == 'POST':
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            raise Http404("Movie not found")
        # Common Django shorcut
        # movie = get_object_or_404(Movie, pk=movie_id)
        WatchlistItem.objects.get_or_create(user=request.user, movie=movie)
    return redirect('movie_list')

@login_required
def remove_from_watchlist(request, movie_id):
    if request.method == 'POST':
        WatchlistItem.objects.filter(user=request.user, movie_id=movie_id).delete()
    return redirect(request.META.get('HTTP_REFERER', 'watchlist_home'))

@login_required
def edit_watchlist_item(request, item_id):
    item = get_object_or_404(WatchlistItem, pk=item_id, user=request.user)
    return render(request, 'watchlist/edit_watchlist_item.html', {'item': item})

@login_required
def update_watchlist_item(request, item_id):
    item = get_object_or_404(WatchlistItem, pk=item_id, user=request.user)
    if request.method == 'POST':
        item.status = request.POST.get('status')
        item.rating = request.POST.get('rating') or None
        item.is_favorite = 'is_favorite' in request.POST
        item.save()
    return redirect('watchlist_home')
