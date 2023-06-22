from django.urls import path
from account.views import (UserRegistrationView, UserLoginView, UserDashboardView, 
UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('send-password-reset-email/', SendPasswordResetEmailView.as_view(), name='send-password-reset-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),

]
