from django.urls import path, include
from . import views

urlpatterns = [
     path('', views.Search_Event.as_view(), name='homepage'),
     path('getCity', views.getCity, name= "get-city"),
     path('category', views.get_category_event, name= "category"),
]
