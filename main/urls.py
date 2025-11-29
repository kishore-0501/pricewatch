from django.urls import path
from .views import signup, home, product_compare, product_list,search_product
from . import views

urlpatterns = [
    path("", home, name="home"),
    path("signup/", signup, name="signup"),
    path('products/', product_list, name='product_list'),
    path('products/<int:id>/', views.product_compare, name='productcompare'),
    path('search/', views.search_product, name='search_product'),
]
