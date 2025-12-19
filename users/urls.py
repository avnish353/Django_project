from django.urls import path,include
from users import views as users_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/" , users_views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="homepage.html"), name="logout"),
    path("forgot-password/", users_views.send_otp, name="send_otp"),
      path("verify-otp/", users_views.verify_otp, name="verify_otp"),
]
