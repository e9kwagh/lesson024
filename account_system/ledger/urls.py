from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("loginpage/", views.loginpage, name="loginpage"),
    path("logoutUser/", views.logoutUser, name="logoutUser"),
    path("report/", views.report, name="report"),
    path("signuppage/", views.signuppage, name="signuppage"),
    path("transaction/", views.transaction, name="transaction"),
]
