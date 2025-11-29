from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Product
from .forms import SignupForm, LoginForm
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import ebay_client, amazon_rapidapi
from django.utils.text import slugify
from decimal import Decimal
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import boto3
from boto3.dynamodb.conditions import Key
from django.contrib import messages
from price_comparator.validators import find_least_price


db_client = boto3.resource('dynamodb')
product_table=db_client.Table('Products')
price_table = db_client.Table('Prices')




def home(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()
    return render(request, "main/home.html", {
        "products": products,
        "query": query
    })
    



def signup(request):
    print('0')
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print('4')
            user = form.save()  # Save the user
            # Automatically log in the new user
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            print("user name ")
            user = authenticate(username=username, password=raw_password)
            print('1')
            login(request, user)
            print('2')
            return redirect("/")  # Redirect to home page
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})
    

def product_detail(request, id):
    response = product_table.scan()
    products = response.get('Items', [])
    return render(request, 'product_detail.html', {'product': product})
    



def price_fetch(id):
    product_id = str(id)

    # Fetch product
    response = product_table.get_item(Key={'product_id': id})
    product = response.get('Item')

    if not product:
        return render(request, 'product/not_found.html', {'product_id': id})

    return product
    

def product_compare(request, id):

    price_response = price_table.query(
        KeyConditionExpression=Key('product_id').eq(str(id))
    )
    prices = price_response.get('Items', [])
    print(prices)
    leastPrice = find_least_price(prices)
    print('least Price = ',leastPrice['price'])
    # Debug print
    for p in prices:
        print(f"Vendor: {p['vendor']}, Price: {p['price']}")

    product =  {
        'product_id': '1',
        'name': 'iPhone 17 Pro',
        'description': 'Latest Apple iPhone model',
        'image': 'https://price-comparator-bucket.s3.us-east-1.amazonaws.com/iPhone17.jpg'
    }
    return render(request, 'product/compare.html', {
        'product': product,
        'prices': prices,
        'least_price':leastPrice['price'],
        'vendor':leastPrice['vendor']
    })

def search_product(request):
    query = request.GET.get('q', '')

    try:
        product = Product.objects.get(name__icontains=query)
        print('2')
        return redirect('productcompare', id=product.id)
    except Product.DoesNotExist:
        return render(request, 'search_not_found.html', {'query': query})
