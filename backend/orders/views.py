from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartItem

from .models import Order, OrderItem
from .serializers import CheckoutSerializer, OrderSerializer


class OrderListView(generics.ListAPIView):
    """GET /api/orders/ - the current user's order history (or all orders for admins)."""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Order.objects.prefetch_related('items__product')
        if user.is_staff and self.request.query_params.get('all') == 'true':
            return qs.all()
        return qs.filter(user=user)


class OrderDetailView(generics.RetrieveAPIView):
    """GET /api/orders/<id>/"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Order.objects.prefetch_related('items__product')
        return qs if user.is_staff else qs.filter(user=user)


class OrderStatusUpdateView(APIView):
    """PATCH /api/orders/<id>/status/ - admin updates an order's fulfillment status."""
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'detail': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)


class CheckoutView(APIView):
    """POST /api/orders/checkout/ - converts the current cart into an Order.

    Stock is decremented and the cart cleared atomically so a failure
    midway never leaves stock or the cart in an inconsistent state.
    """
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
        if not cart_items.exists():
            return Response({'detail': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                return Response(
                    {'detail': f'Not enough stock for {cart_item.product.name}.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        total_amount = sum(item.subtotal for item in cart_items)
        order = Order.objects.create(
            user=request.user, total_amount=total_amount, status='pending', **serializer.validated_data
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
            )
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()

        cart_items.delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
