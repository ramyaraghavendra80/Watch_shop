from django.shortcuts import render, get_object_or_404, redirect
from .models import Watchlist, Wishlist, Cart, Review, Profile
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
from django.contrib.auth import login, authenticate
from .forms import SignupForm, WatchForm, ProfileForm, CustomLoginForm, ReviewForm
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.db.models import Q


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')

            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True
            user.save()

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


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def Home(request):
    # Check if the user is authenticated before accessing their cart
    user_cart_items = []
    if request.user.is_authenticated:
        user_cart_items = Cart.objects.filter(
            user=request.user).values_list('watch_id', flat=True)

    # Fetch all watches
    watches = Watchlist.objects.all()  # Or any filtering you want
    context = {
        'watches': watches,
        'user_cart_items': user_cart_items,
    }
    return render(request, 'home.html', context)


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
    user_cart_items = Cart.objects.filter(user=request.user).values_list(
        'watch_id', flat=True)  # Fetch watch IDs in the user's cart

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
        'user_cart_items': user_cart_items,

    }
    return render(request, 'watchdetails.html', context)


@login_required
@admin_required
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

    return redirect('home', watch_id=watch_id)


# View wishlist
@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def add_to_cart(request, watch_id):
    watch = get_object_or_404(Watchlist, id=watch_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user, watch=watch
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('watchdetail', watch_id=watch_id)


@login_required
def update_cart(request, cart_id):
    # Get the specific cart item for the user
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if request.method == "POST":
        # Get the new quantity from the form, defaulting to 1 if not provided
        quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('cartlist')  # Redirect to the cart page


@login_required
def remove_from_cart(request, cart_id):
    # Get the specific cart item for the user and delete it
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cartlist')  # Redirect to the cart page


@login_required
def cartlist_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = 0
    total_items_count = 0

    # Calculate total price with discount for each item in the cart
    for item in cart_items:
        original_price = item.watch.price
        discount = item.watch.discount
        discounted_price = original_price * (discount / 100)
        total_item_price = original_price - discounted_price
        # Calculate total price for this item
        item.total_item_price = total_item_price * item.quantity
        # Update overall totals
        total_price += item.total_item_price
        total_items_count += item.quantity

        item.discounted_price = discounted_price
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items_count': total_items_count,
    }
    return render(request, 'cartlist.html', context)


@login_required
def buy_now(request, watch_id):
    watch_detail = get_object_or_404(Watchlist, id=watch_id)
    return render(request, 'buynow.html', {'watch_detail': watch_detail})


@login_required
def payment_page(request):
    return render(request, 'payment.html')


@login_required
def payment_success(request):
    messages.success(request, "Order placed successfully!")
    return render(request, 'paymentsuccess.html')


@login_required
def search_view(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        results = Watchlist.objects.filter(
            Q(brand__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query)
        )
        results_data = [{'id': watch.id, 'title': watch.brand,
                         'price': watch.price} for watch in results]
        return JsonResponse(results_data, safe=False)

    return JsonResponse([], safe=False)
