from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.illuminance_chart, name='illuminance_chart'),
    path('create_graph/', views.create_graph, name='create_graph'),
    path('api/save_illuminance_data/', views.save_illuminance_data),
    path('api/room_status/', views.room_status, name='room_status'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]