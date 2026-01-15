from django.contrib import admin
from django.urls import path
from authenticate import views

urlpatterns = [
    
    path('signup/', views.user_sign_in, name='signup'),
    path('login/', views.user_log_in, name='login'),
    path('logout/', views.user_logout_in, name='logout'),
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),
    path('request-reset-email/', views.RequestResetEmailView.as_view(), name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>/', views.SetNewPasswordView.as_view(), name='set-new-password'),

]
