from django.contrib import admin
from django.urls import path, include
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('index/<int:smoothie_id>/', views.index, name='index_smoothie_id'),
    path('register/', views.register, name='register'),
    path('create_smoothie/', views.create_smoothie, name='create_smoothie'),
    path('view_smoothie/<int:smoothie_id>/',
         views.view_smoothie, name='view_smoothie'),
    path('list_smoothies/', views.list_smoothies, name='list_smoothies'),
    path('mysmoothies/<int:smoothie_id>/', views.index, name='index_smoothie'),
]
