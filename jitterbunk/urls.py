from django.contrib import admin
from django.urls import path
from bunk import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_feed, name='main_feed'),
    path('user/<str:username>', views.personal_feed, name='personal_feed'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]