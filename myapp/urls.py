from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('', views.IndexView.as_view(), name='index'),

]
