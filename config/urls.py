from django.contrib import admin
from django.urls import path
from accounts import views
urlpatterns=[path('',views.index),path('login/',views.index),path('signup/',views.index),path('dashboard/',views.index),path('index.html',views.index),path('login.html',views.index),path('signup.html',views.index),path('dashboard.html',views.index),path('admin/',admin.site.urls),path('api/session/',views.session),path('api/signup/',views.signup),path('api/login/',views.signin),path('api/logout/',views.signout),path('api/watchlist/',views.watchlist)]
