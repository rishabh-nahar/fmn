from django.conf.urls.static import static
from findmynotes import settings
from . import views
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('', views.home , name = "home"),
    path('profile/', views.profile , name = "profile"),
    path('upload/', views.upload , name = "upload"),
    path('feed/', views.feed , name = "feed"),
    path('search_page/', views.search_page , name = "search_page"),
    path('searched_page/<slug:search_obj>', views.searched_page , name = "searched_page"),
    path('approve_file/', views.approve_file , name = "approve_file"),
    path('otp_page/', views.otp_page , name = "otp_page"),
    path('login/', views.login , name = "login"),
    path('registration/', views.registration , name = "registration"),
    path('logout/', views.logout , name = "logout"),
]
