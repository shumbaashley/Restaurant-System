from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from restaurants.forms import UserForm, RestaurantForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return redirect(restaurant_home)

    #return render(request, 'restaurant/base.html', {})

def sign_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "restaurant/sign_in.html", {})

def sign_out(request):
    logout(request)
    return render(request, "restaurant/sign_in.html", {})

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



@login_required(login_url='/restaurant/sign-in')
def restaurant_home(request):
    return render(request, 'restaurant/base.html')


@login_required(login_url='/restaurant/sign-in')
def restaurant_account(request):
    return render(request, 'restaurant/account.html', {})


@login_required(login_url='/restaurant/sign-in')
def restaurant_meal(request):
    return render(request, 'restaurant/meal.html', {})


@login_required(login_url='/restaurant/sign-in')
def restaurant_order(request):
    return render(request, 'restaurant/order.html', {})


@login_required(login_url='/restaurant/sign-in')
def restaurant_report(request):
    return render(request, 'restaurant/report.html', {})