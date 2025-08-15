from django.urls import path
from . import views
from django.views.generic import TemplateView

from .api import ProfileListAPIView, ProfileDetailAPIView



urlpatterns = [
   path('', TemplateView.as_view(template_name='home.html'),name='home'),
   path('register/' , views.UserRegisterView.as_view() , name='register'),
   path('login/' , views.UserLoginView.as_view() , name='login_page'),
   path('logout/' , views.UserLogoutView.as_view() , name='logout'),
   path('edit-register/' , views.UserEditeRegisterView.as_view() , name='edit_register'),
   path('change-password/' , views.UserChangePasswordView.as_view() , name='change_password'),
   path('profile/<int:pk>/' , views.UserProfilePageView.as_view() , name='profile_page'),
   path('edit_profile/<int:pk>/' , views.UserEditProfilePageView.as_view() , name='edit_profile_page'),
   
   
   path('api/profile-list', ProfileListAPIView.as_view(), name="profile-list-api"),
   path('api/profile-list/<int:pk>/', ProfileDetailAPIView.as_view(), name="profile-detail-api")

   
     
]