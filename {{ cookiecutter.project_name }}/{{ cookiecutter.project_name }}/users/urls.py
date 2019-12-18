from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "user"

urlpatterns = [
  path('register/', views.UserCreateView.as_view(), name="register"),
  path('login/', views.UserLoginView.as_view(), name="login"),
  path('logout/', LogoutView.as_view(), name="logout"),
  path('~redirect/', views.UserRedirectView.as_view(), name="redirect"),
  path('<username>/', views.UserDetailView.as_view(), name="detail"),
  path('<username>/update-account/', views.UserUpdateView.as_view(), name="update_account"),
  path('<username>/delete-account/', views.UserDeleteView.as_view(), name="delete_account"),
  path('<username>/change-password/', views.UserPasswordChangeView.as_view(), name="password_change"),
]


