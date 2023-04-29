"""inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.home, name="home"),
    path('dash/', views.dash, name="dash"),
    path('load/',views.index, name="index"),
    path('mojos-tampa/', views.clone, name="clone"),
    path('item/<str:pk>',views.item, name="item"),
    path('mojos-mp/', views.mojos, name="mojos"),
    #path('products/', views.products, name="products"),
    path('products/',views.topProducts, name="products"),
    path("getstarted/", views.getstarted, name="getstarted"),
    path('profile/<str:pk>/', views.employeeprofile, name="employee"),
#    path('register/', views.Register, name="create_user" ),
    path('register/', views.signUp, name="create_user" ),

#    path('addprod/', views.addProd, name="addprod"),
    path('addprod/', views.addProduct, name="addprod"),
    path('search/', views.searchprod, name="search"),
    path('mj-search/', views.search, name="mjsearch"),

    path('updateuser/<str:pk>', views.updateUser, name="updateuser"),
 #   path('login/', views.loginPage, name="login"),
    path('login/', views.logIn, name="login"),

    path('deleteuser/<str:pk>', views.deleteUser, name="deleteuser"),
    path('updateprod/<str:pk>', views.updateProd, name="updateprod"),
    path('deleteprod/<str:pk>', views.deleteProduct, name="deleteprod"),

]
 