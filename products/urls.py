from django.urls import path
from . import views

urlpatterns = [
    path('products/<slug:slug>/', views.get_product, name="get_product"),
]
