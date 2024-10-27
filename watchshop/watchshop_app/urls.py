from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('navbar', views.Navbar, name="navbar"),
    # path('/about', views.About, name="about"),
    path('watch/<int:watch_id>/', views.Watchdetail, name='watchdetail'),
    path('add_watch/', views.Add_watch, name='add_watch'),
    path('watchlist/', views.watchlist_view, name='watchlist'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('add_to_wishlist/<int:watch_id>/',
         views.add_to_wishlist, name='add_to_wishlist'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('add_to_cart/<int:watch_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:cart_id>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('cartlist/', views.cartlist_view, name='cartlist'),
    path('buy_now/<int:watch_id>/', views.buy_now, name='buy_now'),
    path('payment/', views.payment_page, name='payment_page'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('search/', views.search_view, name='search_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
