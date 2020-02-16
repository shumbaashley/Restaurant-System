from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from restaurants.forms import UserForm, RestaurantForm, UserFormForEdit, MealForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Meal, Order

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'restaurant/login.html', {"message": None})

    return redirect(order)

@login_required
def account (request):
    user_form = UserFormForEdit(instance = request.user)
    restaurant_form = RestaurantForm(instance = request.user.restaurant)

    if request.method == "POST":
        user_form = UserFormForEdit(request.POST, instance = request.user)
        restaurant_form = RestaurantForm(request.POST, request.FILES, instance = request.user.restaurant)

        if user_form.is_valid() and restaurant_form.is_valid():
            user_form.save()
            restaurant_form.save()


    return render(request, 'restaurant/account.html', {
        "user_form": user_form,
        "restaurant_form": restaurant_form
    })

@login_required
def restaurant_meal (request):
    meals = Meal.objects.filter(restaurant = request.user.restaurant).order_by("id") 

    return render(request, 'restaurant/meal.html', {"meals" : meals})

@login_required
def add_meal (request):
    form = MealForm()
    if request.method == "POST":
        form = MealForm(request.POST, request.FILES)

        if form.is_valid():
            meal = form.save(commit=False)
            meal.restaurant = request.user.restaurant
            meal.save()  
            return redirect(restaurant_meal)

    return render(request, 'restaurant/add_meal.html', {
        "form" : form
    })

@login_required
def edit_meal (request, meal_id):
    form = MealForm(instance = Meal.objects.get(id = meal_id))

    if request.method == "POST":
        form = MealForm(request.POST, request.FILES, instance = Meal.objects.get(id = meal_id))

        if form.is_valid():
            form.save()  
            return redirect(restaurant_meal)

    return render(request, 'restaurant/edit_meal.html', {
        "form" : form
    })

@login_required
def order (request):

    if request.method == "POST":
        order = Order.objects.get(id = request.POST["id"], restaurant = request.user.restaurant )

        if order.status == Order.COOKING:
            order.status = Order.READY
            order.save()


    orders = Order.objects.filter(restaurant = request.user.restaurant).order_by("-id")
    return render(request, 'restaurant/order.html', {
        "orders" : orders
    })

@login_required
def report (request):
    from datetime import datetime, timedelta

    revenue = []
    orders = []


    today = datetime.now()
    current_weekdays = [today + timedelta(days = i) for i in range(0 - today.weekday(), 7 - today.weekday() )]

    for day in current_weekdays:
        delivered_orders = Order.objects.filter(
            restaurant = request.user.restaurant,
            status = Order.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )

        revenue.append(sum(order.total for order in delivered_orders))
        orders.append(delivered_orders.count())

    return render(request, 'restaurant/report.html', {
        "revenue": revenue,
        "orders" : orders
    })

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, 'restaurant/login.html', {"message": "Invalid Credentials"})

def logout_view(request):
    logout(request)
    return render(request, 'restaurant/login.html', {"message": "Logged Out"})

def sign_up(request):
    user_form = UserForm()
    restaurant_form = RestaurantForm()

    if request.method == "POST":
        user_form  = UserForm(request.POST)
        restaurant_form = RestaurantForm(request.POST, request.FILES)

        if user_form.is_valid() and restaurant_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_restaurant = restaurant_form.save(commit=False)
            new_restaurant.user = new_user
            new_restaurant.save()

            login(request, authenticate(
                username = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]
            ))

            return redirect(home)

    return render(request, 'restaurant/sign_up.html', {
        "user_form": user_form,
        "restaurant_form": restaurant_form
    })



