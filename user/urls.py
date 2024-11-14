from django.urls import path
from . views import SignUpView, sign_out
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("sign_up/", SignUpView.as_view(template_name="user/sign_up.html"), name="sign_up"),
    path("sign_in/", LoginView.as_view(template_name="user/sign_in.html"), name="sign_in"),
    path("sign_out/", sign_out, name="sign_out")
]