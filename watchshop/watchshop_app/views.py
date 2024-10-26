from django.shortcuts import render, get_object_or_404, redirect
from .models import Watchlist, Wishlist, Cart, Review  # Import the Watch model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import SignupForm, WatchForm, ProfileForm, CustomLoginForm, ReviewForm
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import Group


# User registration view


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if form.is_valid() and profile_form.is_valid():
            # Save user first
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')  # Get the role from the form

            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True  # Assign admin rights
            user.save()  # Save the user object

            # Assign user to appropriate group
            if role == 'user':
                # Ensure 'User' group exists
                group = Group.objects.get(name='User')
            elif role == 'admin':
                # Ensure 'Admin' group exists
                group = Group.objects.get(name='Admin')
            user.groups.add(group)

            # Save profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, 'Signup successful! Please log in.')
            # Redirect to the login page after successful signup
            return redirect('login')
        else:
            # If form is not valid, show error messages
            for error in form.errors.values():
                messages.error(request, error)
            for error in profile_form.errors.values():
                messages.error(request, error)
    else:
        form = SignupForm()
        profile_form = ProfileForm()

    return render(request, 'signup.html', {'form': form, 'profile_form': profile_form})


@login_required
def profile_view(request):
    # Get or create profile for the user if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)

    form_display = False  # Variable to control form visibility

    if request.method == 'POST':
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')  # Redirect after updating the profile
        form_display = True  # Display form in case of invalid form submission
    else:
        profile_form = ProfileForm(instance=profile)

    context = {
        'profile_form': profile_form,
        'profile': profile,
        'form_display': form_display
    }
    return render(request, 'profile.html', context)


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


def watchlist_view(request):
    watches = Watchlist.objects.all()
    user_wishlist_items = Wishlist.objects.filter(
        user=request.user).values_list('watch_id', flat=True)

    return render(request, 'watchlist.html', {'watches': watches, 'user_wishlist_items': user_wishlist_items})


def Navbar(request):
    return render(request, 'navbar.html')


@login_required
def Watchdetail(request, watch_id):
    watch_detail = get_object_or_404(Watchlist, id=watch_id)
    reviews = watch_detail.reviews.all()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            # Create review instance without saving to DB
            review = review_form.save(commit=False)
            review.user = request.user  # Set the user
            review.watch = watch_detail  # Set the watch

            # Validation logic
            if Review.objects.filter(user=review.user, watch=review.watch).exists():
                review_form.add_error(
                    None, "You have already reviewed this watch.")
            else:
                try:
                    review.full_clean()  # Validate the review
                    review.save()  # Save the review if validation passes
                    return redirect('watchdetail', watch_id=watch_id)
                except ValidationError as e:
                    # Add error to form if it fails
                    review_form.add_error(None, e)
        else:
            # If the form is not valid, add the form errors to the form
            for field, errors in review_form.errors.items():
                for error in errors:
                    review_form.add_error(field, error)
    else:
        review_form = ReviewForm()

    context = {
        'watch_detail': watch_detail,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'watchdetails.html', context)


def Add_watch(request):
    if request.method == 'POST':
        form = WatchForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the current item

            # Check if the 'Save and Add Another' button was clicked
            if 'add_another' in request.POST:
                form = WatchForm()  # Create a new empty form for the next item
            else:
                # Redirect to the home page if not adding another
                return redirect('home')
    else:
        form = WatchForm()  # Create a new form instance if GET request

    return render(request, 'add_watch.html', {'form': form})

# Add to wishlist


@login_required
def add_to_wishlist(request, watch_id):
    watch = Watchlist.objects.get(id=watch_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user, watch=watch)

    if not created:
        wishlist_item.delete()

    return redirect('watchlist')


# View wishlist
@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def add_to_cart(request, watch_id):
    watch = get_object_or_404(Watchlist, id=watch_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user, watch=watch)

    if not created:
        # If the item already exists, just increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect('watchlist')  # Redirect to the watchlist or cart page


@login_required
def update_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('cartlist')  # Redirect to the cart page


@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cartlist')  # Redirect to the cart page


@login_required
def cartlist_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.watch.price * item.quantity for item in cart_items)
    total_items_count = sum(item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items_count': total_items_count,
    }
    return render(request, 'cartlist.html', context)
