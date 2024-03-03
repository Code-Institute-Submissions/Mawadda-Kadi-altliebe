from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, View
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import UserRegisterForm, ProfileForm


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)  # Authenticate the user
            if user is not None:
                login(request, user)  # Log the user in
                messages.success(request, f'Account created for {username}! You are now able to log in')
                return redirect('user-profile', username=username)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('user-profile', kwargs={'username': username})


@login_required
def profile(request):
    # Passes the user's own profile to the template
    return render(request, 'users/profile.html', {'profile': request.user.profile, 'own_profile': True})

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    # Checks if the requested profile belongs to the logged-in user
    own_profile = request.user == user
    return render(request, 'users/profile.html', {'profile': user.profile, 'own_profile': own_profile})


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile_edit.html'
    success_url = reverse_lazy('user-profile')

    def get_object(self):
        return self.request.user.profile

class DeleteAccount(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        # Consider adding additional checks (e.g., re-authentication)
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('product-list')