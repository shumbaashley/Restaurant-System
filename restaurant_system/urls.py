from django.contrib import admin
from django.urls import path, re_path, include
from restaurants import views
from django.conf.urls.static import static
from django.conf import settings
from restaurants.views import account, restaurant_meal, order, report, edit_meal, add_meal
from restaurants import apis


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('sign_up', views.sign_up , name="sign-up"),


    path('account', views.account, name='restaurant-account'),
    path('meal', views.restaurant_meal, name='restaurant-meal'),
    path('meal/add/', views.add_meal, name='restaurant-add-meal'),
    re_path(r'^meal/edit/(?P<meal_id>\d+)/$', views.edit_meal, name='restaurant-edit-meal'),    
    path('order', views.order, name='restaurant-order'),
    path('report', views.report, name='restaurant-report'),

    re_path(r'^api/social/', include('rest_framework_social_oauth2.urls')),

    # API for Customers
    path('api/customer/restaurants/', apis.customer_get_restaurants),
    re_path(r'^api/customer/meals/(?P<restaurant_id>\d+)/$', apis.customer_get_meals),
    path('api/customer/order/add/', apis.customer_add_order),
    path('api/customer/order/latest/', apis.customer_get_latest_order),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
