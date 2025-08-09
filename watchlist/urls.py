from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path('movies/', views.movie_list, name='movie_list'),
    path('add-to-watchlist/<int:movie_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove-from-watchlist/<int:movie_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('watchlist/', views.watchlist_home, name='watchlist_home'),
    path('watchlist/edit/<int:item_id>/', views.edit_watchlist_item, name='edit_watchlist_item'),
    path('watchlist/update/<int:item_id>/', views.update_watchlist_item, name='update_watchlist_item'),
    path('api/search-movies/', views.search_movies, name='search_movies'),
    path('api/add-movie-from-tmdb/<int:tmdb_id>/', views.add_movie_from_tmdb, name='add_movie_from_tmdb'),




]
