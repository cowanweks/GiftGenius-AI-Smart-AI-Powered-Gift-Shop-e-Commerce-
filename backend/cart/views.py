from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CartItem
from .serializers import CartItemSerializer


class CartView(APIView):
    """GET /api/cart/ - list items. POST /api/cart/ - add an item (or bump quantity)."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = CartItem.objects.filter(user=request.user).select_related('product')
        serializer = CartItemSerializer(items, many=True, context={'request': request})
        total = sum(item.subtotal for item in items)
        return Response({'items': serializer.data, 'total': total})

    def post(self, request):
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))
        item, created = CartItem.objects.get_or_create(
            user=request.user, product_id=product_id, defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()
        serializer = CartItemSerializer(item, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemDetailView(APIView):
    """PATCH /api/cart/<id>/ - update quantity. DELETE /api/cart/<id>/ - remove item."""
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request, pk):
        return CartItem.objects.get(pk=pk, user=request.user)

    def patch(self, request, pk):
        item = self.get_object(request, pk)
        quantity = int(request.data.get('quantity', item.quantity))
        if quantity <= 0:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        item.quantity = quantity
        item.save()
        serializer = CartItemSerializer(item, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, pk):
        item = self.get_object(request, pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartClearView(APIView):
    """DELETE /api/cart/clear/ - empty the cart, used after a successful checkout."""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
