from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ProductFilter
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductWriteSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff


class CategoryListView(generics.ListAPIView):
    """GET /api/products/categories/"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class ProductListCreateView(generics.ListCreateAPIView):
    """GET /api/products/ - browse/search/filter/sort products.
    POST /api/products/ - admin creates a product.
    """
    queryset = Product.objects.select_related('category').all()
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'rating', 'created_at', 'name']
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        return ProductWriteSerializer if self.request.method == 'POST' else ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE /api/products/<slug>/"""
    queryset = Product.objects.select_related('category').all()
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        return ProductWriteSerializer if self.request.method in ('PUT', 'PATCH') else ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class TrendingProductsView(generics.ListAPIView):
    """GET /api/products/trending/"""
    queryset = Product.objects.filter(is_trending=True)[:8]
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_serializer_context(self):
        return {'request': self.request}


class FeaturedProductsView(generics.ListAPIView):
    """GET /api/products/featured/"""
    queryset = Product.objects.filter(is_featured=True)[:8]
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_serializer_context(self):
        return {'request': self.request}


class SalesStatsView(APIView):
    """GET /api/products/stats/ - lightweight stats for the admin dashboard."""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        from django.db.models import Sum
        from orders.models import Order, OrderItem
        from users.models import User

        total_orders = Order.objects.count()
        total_revenue = Order.objects.filter(status='completed').aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        total_users = User.objects.count()
        total_products = Product.objects.count()
        low_stock = Product.objects.filter(stock__lte=5).count()
        best_sellers = (
            OrderItem.objects.values('product__name')
            .annotate(units_sold=Sum('quantity'))
            .order_by('-units_sold')[:5]
        )
        return Response({
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'total_users': total_users,
            'total_products': total_products,
            'low_stock_products': low_stock,
            'best_sellers': list(best_sellers),
        })
