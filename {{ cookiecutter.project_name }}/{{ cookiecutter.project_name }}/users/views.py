from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    RedirectView,
    UpdateView,
)
from .forms import CreateUserForm, UpdateUserForm

User = get_user_model()


class PermissionMixin(UserPassesTestMixin):
    """
  Mixin to see whether a user has permission or not. Permission will be granted
  if test_func returns True. If False, a permission error is raised.
  """

    def test_func(self):
        username = self.kwargs["username"]
        if username != self.request.user.username:
            return False
        else:
            return True


class UserCreateView(CreateView):
    template_name = "registration/register.html"
    form_class = CreateUserForm

    def get(self, request, *args, **kwargs):
        """ Redirect to detail page if user is logged in. """
        if request.user.is_authenticated:
            return redirect(reverse("user:detail", kwargs={"username": request.user}))
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """ Login user after account is created. """
        form.save()
        username = self.request.POST["username"]
        password = self.request.POST["password2"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("user:detail", kwargs={"username": self.request.user})


class UserDetailView(DetailView):
    template_name = "users/detail.html"

    def get(self, request, *args, **kwargs):
        """ Only show profile if user is active. """
        user = self.get_object()
        if user.is_active:
            return super().get(request, *args, **kwargs)
        else:
            raise Http404("User does not exist!")

    def get_object(self, queryset=None):
        """ Prevent duplicate queries when retrieving object in other methods. """
        if not hasattr(self, "object"):
            username = self.kwargs["username"]
            user = get_object_or_404(User, username=username)
            self.object = user
        return self.object


class UserLoginView(LoginView):
    template_name = "registration/login.html"

    def get(self, request, *args, **kwargs):
        """ Redirect to detail page if user is logged in. """
        if request.user.is_authenticated:
            return redirect(reverse("user:detail", kwargs={"username": request.user}))
        else:
            return super().get(request, *args, **kwargs)


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """ Used by LOGIN_REDIRECT_URL in settings/base.py """

    def get_redirect_url(self):
        return reverse("user:detail", kwargs={"username": self.request.user})


class UserUpdateView(LoginRequiredMixin, PermissionMixin, UpdateView):
    template_name = "users/update.html"
    form_class = UpdateUserForm

    def get_object(self, queryset=None):
        username = self.kwargs["username"].lower()
        user = get_object_or_404(User, username=username)
        return user


class UserDeleteView(LoginRequiredMixin, PermissionMixin, DeleteView):
    def get(self, request, *args, **kwargs):
        """ Soft deletion by changing user.is_active to False. """
        username = kwargs["username"]
        user = get_object_or_404(User, username=username)
        user.is_active = False
        user.save()
        messages.success(request, "User has been deleted.")
        return redirect(reverse("index"))


class UserPasswordChangeView(LoginRequiredMixin, PermissionMixin, PasswordChangeView):
    def get_success_url(self):
        messages.success(self.request, "Password has been changed.")
        return reverse("user:detail", kwargs={"username": self.request.user})

