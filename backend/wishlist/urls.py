from django.urls import path

from . import views

urlpatterns = [
    path('', views.WishlistView.as_view(), name='wishlist'),
    path('<int:pk>/', views.WishlistItemDetailView.as_view(), name='wishlist-item-detail'),
    path('<int:pk>/move-to-cart/', views.MoveToCartView.as_view(), name='wishlist-move-to-cart'),
]
