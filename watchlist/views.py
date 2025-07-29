from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import UserForm
from .models import WatchlistItem

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