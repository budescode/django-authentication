from django.urls import include, path

from .views import ResetPasswordCodeView, ResetPasswordView, UserLoginView, UserCreateView

urlpatterns = [
    
    path('createuser/', UserCreateView.as_view(), name='create-user'),

    path('login/', UserLoginView.as_view(), name='user-login'),

    path('reset-password-code/', ResetPasswordCodeView.as_view(), name='reset-passwordcode'),

    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),


    
]