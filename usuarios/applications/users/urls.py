from django.urls import path

# from usuarios.applications.home import views

from .views import (
    UserRegisterView, LoginUser, LogoutView, UpdatePasswordView,
    CodeVerificationView
)

app_name = 'users_app'

urlpatterns = [
    path('register/', view=UserRegisterView.as_view(), name='register-user'),
    path('login/', view=LoginUser.as_view(), name='login'),
    path('logout/', view=LogoutView.as_view(), name='logout'),
    path('update/', view=UpdatePasswordView.as_view(), name='update-password'),
    path('verificated/<pk>/', view=CodeVerificationView.as_view(), name='verificated'),
]
