# ownership_transfer/urls.py

from django.urls import path
from .views import register , login_view, account_home,logout_view,add_smartphone,add_smartphone_page,transfer_ownership,home
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('accounts/', views.account_home, name='account_home'),
    path('logout/', views.logout_view, name='logout'),
    path('add_smartphone/', views.add_smartphone, name='add_smartphone'),
    path('add_smartphone_page/',views.add_smartphone_page, name='add_smartphone_page'),
    path('transfer_ownership/<int:ownership_id>/',views.transfer_ownership,name='transfer_ownership'),
    path('home/', home, name='home'),



]
