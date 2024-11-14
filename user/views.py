from django.shortcuts import render
from django.contrib.auth.models import User
from . forms import SignUpForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib import messages


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('sign_in')

    def get_success_url(self) -> str:
        messages.success(self.request, f"Account created successfully!")
        return super().get_success_url()



def sign_out(request):
    logout(request)
    return render(request, "user/sign_out.html")
