from django.contrib import admin
from django.urls import path, include
from restaurants import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # Restaurant
    path('restaurant/sign-in', views.sign_in, name="restaurant-sign-in"),
    path('restaurant/sign-out', views.sign_out, name="restaurant-sign-out"),
    path('restaurant/sign-up', views.sign_up , name="restaurant-sign-up"),
    #path('restaurant/', views.restaurant_home , name="restaurant_home"),

    path('restaurant/account', views.restaurant_account, name='restaurant-account'),
    path('restaurant/meal', views.restaurant_meal, name='restaurant-meal'),
    path('restaurant/order', views.restaurant_order, name='restaurant-order'),
    path('restaurant/report', views.restaurant_report, name='restaurant-report'),


    # Sign In/ Sign Up/ Sign Out
    path('api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign in/ sign up)
    # /revoke-token (sign out)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
