from django.urls import path

from . import views

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('clear/', views.CartClearView.as_view(), name='cart-clear'),
    path('<int:pk>/', views.CartItemDetailView.as_view(), name='cart-item-detail'),
]
