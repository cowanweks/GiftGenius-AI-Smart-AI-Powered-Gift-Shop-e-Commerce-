from rest_framework import serializers

from products.serializers import ProductSerializer

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_detail', 'quantity', 'price', 'subtotal')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'user', 'username', 'total_amount', 'status', 'payment_method',
            'full_name', 'phone_number', 'address', 'city', 'notes',
            'mpesa_reference', 'items', 'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'user', 'total_amount', 'created_at', 'updated_at')


class CheckoutSerializer(serializers.Serializer):
    """Validates the shipping form submitted from the checkout page."""
    full_name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    notes = serializers.CharField(required=False, allow_blank=True)
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES)
