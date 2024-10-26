from django import forms
from .models import Watchlist, CustomUser, Profile, Review
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES,
                             widget=forms.RadioSelect, required=True)

    class Meta:
        model = CustomUser  # Ensure this is the correct user model
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role not in dict(self.ROLE_CHOICES):
            raise forms.ValidationError("Invalid role selected.")
        return role


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        fields = ['username', 'password']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fullname', 'dob', 'phone_number', 'bio', 'profile_pic']


class WatchForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ['brand', 'description', 'price', 'image', 'stock',
                  'discount']  # Include stock and discount fields
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }