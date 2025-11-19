from django.urls import path
from .views import signup, verify_otp, login_view, logout_view, home, product_detail

urlpatterns = [
    path("", home, name="home"),
    path("product/<int:product_id>/", product_detail, name="product_detail"),
    path("signup/", signup, name="signup"),
    path("verify-otp/<str:username>/", verify_otp, name="verify_otp"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
