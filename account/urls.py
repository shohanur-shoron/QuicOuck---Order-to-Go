from django.urls import path
from account import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('sotreSignUp/', views.storeSignUp, name='storeSignUp'),
    path('login/', views.login, name='login'),
    path('logout/', views.logOutUser, name='logOutUser'),
    path('signup/profileCreated', views.createAccount, name='createAccount'),
    path('sotreSignUp/profileCreated', views.createStore, name='createStore'),
    path('loginUser/', views.loginUser, name='loginUser'),
]