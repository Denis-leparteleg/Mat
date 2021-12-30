from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='google_login'),
    path('accounts/', include('allauth.urls')),

]