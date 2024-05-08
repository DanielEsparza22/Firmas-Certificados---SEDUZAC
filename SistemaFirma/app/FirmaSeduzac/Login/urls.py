from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('',views.LoginView.as_view(), name="login"),
    path('logout/',LogoutView.as_view(), name="logout"),
    path('register/', views.RegisterView.as_view(), name='register'),

]