from django.contrib import messages
from django.contrib.auth import (authenticate, get_user_model, login)
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import UpdateView

from .forms import (LoginForm, CustomPasswordChangeForm)

# Create your views here.

User = get_user_model()

class LoginView(generic.FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(email=email, password=password)
        if user is not None:
            if not user.is_active:
                messages.warning(self.request, "Your account has been suspended. Contact admin for more info.")
                return super().form_invalid(form)
                
            login(self.request, user)
            return super().form_valid(form)
        messages.error(self.request, "Invalid email or password")
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return reverse('home_page')
            elif hasattr(user, "teacher"):
                return reverse('assessment:teacher_dashboard_view')
            else:
                pass
                # return reverse('student:course_list')
        return reverse('login')


class SignOutView(LogoutView):
    next_page = reverse_lazy('home_page')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/change_password.html' 
    form_class = CustomPasswordChangeForm 
    success_url = reverse_lazy('accounts:login')
