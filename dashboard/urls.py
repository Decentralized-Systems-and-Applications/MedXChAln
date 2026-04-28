from django.urls import path
from . import views

urlpatterns = [
    # This means the "empty" path (homepage) runs the index function
    path('', views.index, name='index'),
]