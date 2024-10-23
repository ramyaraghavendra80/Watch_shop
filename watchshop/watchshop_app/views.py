from django.shortcuts import render, get_object_or_404, redirect
from .models import Watchlist, Wishlist  # Import the Watch model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, WatchForm, ProfileForm
from django.contrib.auth import logout
from django.contrib import messages

# User registration view


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
        profile_form = ProfileForm()
    return render(request, 'signup.html', {'form': form, 'profile_form': profile_form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(
                request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'profile_form': profile_form})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                # Redirect to home page after successful login
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def Home(request):
    watches = Watchlist.objects.all()  # Fetch all watches
    return render(request, 'home.html', {'watches': watches})


def Navbar(request):
    return render(request, 'navbar.html')


def Watchdetail(request, id):
    watch_detail = get_object_or_404(Watchlist, id=id)
    return render(request, 'watchdetails.html', {'watch_detail': watch_detail})


def Add_watch(request):
    if request.method == 'POST':
        form = WatchForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = WatchForm()

    return render(request, 'add_watch.html', {'form': form})

# @login_required


def Wish_list(request):
    watches = Watch.objects.all()
    user_wishlist = Wishlist.objects.filter(user=request.user).first()
    user_wishlist_items = user_wishlist.watches.all() if user_wishlist else []

    context = {
        'watches': watches,
        'user_wishlist_items': user_wishlist_items,
    }
    return render(request, 'watchlist.html', context)

# @login_required


def add_to_wishlist(request, watch_id):
    watch = get_object_or_404(Watchlist, id=watch_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if watch in Wishlist.watches.all():
        # Remove from wishlist if it already exists
        wishlist.watches.remove(watch)
    else:
        wishlist.watches.add(watch)  # Add to wishlist if it's not there

    return redirect('watchlist')
