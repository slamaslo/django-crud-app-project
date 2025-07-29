from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path('watchlist/', views.watchlist_home, name='watchlist_home'),
]
