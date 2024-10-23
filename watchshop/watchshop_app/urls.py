from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('navbar', views.Navbar, name="navbar"),
    # path('/about', views.About, name="about"),
    path('watch/<int:id>/', views.Watchdetail, name='watchdetail'),
    path('add_watch/', views.Add_watch, name='add_watch'),
    path('watchlist/', views.Watchlist, name='watchlist'),
    path('add_to_wishlist/<int:watch_id>/',
         views.add_to_wishlist, name='add_to_wishlist'),
    path('signup/', views.signup_view, name='signup'),
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
