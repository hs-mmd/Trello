from django.shortcuts import render , redirect
from django.views import generic , View
from django.urls import reverse_lazy
from .forms import RegistrationForm , LoginForm , EditeRegisterForm,ChangePasswordForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import DetailView,UpdateView
from .models import Profile


class UserRegisterView(generic.CreateView):
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login_page')
    
class UserLoginView(View):
    def get(self, request):
        Login_form = LoginForm()
        return render(request=request, template_name='login.html', context={'form' : Login_form})        
    
    def post(self, request):
        Login_form = LoginForm(request.POST)
        if Login_form.is_valid():
            username = Login_form.cleaned_data.get('username')
            password = Login_form.cleaned_data.get('password')
            user = User.objects.filter(username=username).first()
            if user is not None:
                corroct_password = user.check_password(password)
                if corroct_password:
                    login(request, user)
                    return redirect('home')
                else:
                    Login_form.add_error(field='password' , error='password is wrong')
            else:
                Login_form.add_error(field='username' , error='the user not found')
                
        return render(request=request, template_name='login.html', context={'form' : Login_form})        

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class UserEditeRegisterView(generic.UpdateView):
    form_class = EditeRegisterForm
    template_name = 'edit_register.html'
    success_url = reverse_lazy('home')
    
    def get_object(self):
        return self.request.user
    
class UserChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'change_password.html'
    success_url = reverse_lazy('home')
    
    
class UserProfilePageView(DetailView):
    model = Profile
    template_name = "profile_page.html"

class UserEditProfilePageView(UpdateView):
    model = Profile
    template_name = "edit_profile_page.html"
    fields = ['bio', 'picture']
    success_url = reverse_lazy('home')