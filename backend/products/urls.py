from django.urls import path

from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('trending/', views.TrendingProductsView.as_view(), name='product-trending'),
    path('featured/', views.FeaturedProductsView.as_view(), name='product-featured'),
    path('stats/', views.SalesStatsView.as_view(), name='product-stats'),
    path('', views.ProductListCreateView.as_view(), name='product-list'),
    path('<slug:slug>/', views.ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
]
