from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Product, PriceHistory, UserProfile
from .forms import SignupForm, LoginForm
import random


# ---------------------------
# Home Page View (Public)
# ---------------------------
def home(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    product_data = []
    for p in products:
        history = PriceHistory.objects.filter(product=p)
        prices = [h.price for h in history]
        product_data.append({
            'product': p,
            'low_price': min(prices) if prices else 0,
            'high_price': max(prices) if prices else 0,
            'current_price': prices[-1] if prices else 0
        })

    return render(request, "main/home.html", {
        "products": product_data,
        "query": query
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    history = PriceHistory.objects.filter(product=product).order_by("timestamp")

    price_list = [h.price for h in history]
    date_list = [h.timestamp.strftime("%Y-%m-%d") for h in history]

    low_price = min(price_list) if price_list else 0
    high_price = max(price_list) if price_list else 0

    return render(request, "main/product_detail.html", {
        "product": product,
        "price_list": price_list,
        "date_list": date_list,
        "low_price": low_price,
        "high_price": high_price,
    })

# ---------------------------
# STEP 1 — SIGNUP (Store data + send OTP)
# ---------------------------
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Check if username or email exists
            if User.objects.filter(username=username).exists():
                return render(request, "main/signup.html", {
                    "form": form,
                    "error": "Username already exists."
                })

            if User.objects.filter(email=email).exists():
                return render(request, "main/signup.html", {
                    "form": form,
                    "error": "Email already registered."
                })

            # Generate OTP
            otp = random.randint(100000, 999999)

            # Save signup data temporarily in session
            request.session["pending_user"] = {
                "username": username,
                "email": email,
                "password": password,
                "otp": otp,
            }

            # Send OTP email
            send_mail(
                subject="Your PriceWatch OTP",
                message=f"Your OTP is {otp}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return redirect("verify_otp")

    else:
        form = SignupForm()

    return render(request, "main/signup.html", {"form": form})


# ---------------------------
# STEP 2 — OTP Verification (Create user after OTP)
# ---------------------------
def verify_otp(request):
    pending = request.session.get("pending_user")
    if not pending:
        return redirect("signup")

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        if str(entered_otp) == str(pending["otp"]):
            # Create user only after OTP is correct
            user = User.objects.create_user(
                username=pending["username"],
                email=pending["email"],
                password=pending["password"]
            )

            UserProfile.objects.create(user=user, otp_verified=True)

            # Clear pending session
            del request.session["pending_user"]

            return redirect("login")

        return render(request, "main/verify_otp.html", {
            "error": "Incorrect OTP. Try again."
        })

    return render(request, "main/verify_otp.html")


# ---------------------------
# STEP 3 — LOGIN
# ---------------------------
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)
            if user:
                profile = UserProfile.objects.get(user=user)
                if not profile.otp_verified:
                    return redirect("verify_otp")

                login(request, user)
                return redirect("home")

            return render(request, "main/login.html", {
                "form": form,
                "error": "Invalid username or password"
            })

    else:
        form = LoginForm()

    return render(request, "main/login.html", {"form": form})


# ---------------------------
# LOGOUT
# ---------------------------
def logout_view(request):
    logout(request)
    return redirect("home")
