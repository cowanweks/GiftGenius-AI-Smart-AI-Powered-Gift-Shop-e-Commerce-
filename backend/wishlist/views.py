from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartItem

from .models import WishlistItem
from .serializers import WishlistItemSerializer


class WishlistView(APIView):
    """GET /api/wishlist/ - list saved products. POST /api/wishlist/ - save a product."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = WishlistItem.objects.filter(user=request.user).select_related('product')
        serializer = WishlistItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product')
        item, created = WishlistItem.objects.get_or_create(user=request.user, product_id=product_id)
        serializer = WishlistItemSerializer(item, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class WishlistItemDetailView(APIView):
    """DELETE /api/wishlist/<id>/ - remove a saved product."""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        WishlistItem.objects.filter(pk=pk, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MoveToCartView(APIView):
    """POST /api/wishlist/<id>/move-to-cart/ - move a saved product into the cart."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            item = WishlistItem.objects.get(pk=pk, user=request.user)
        except WishlistItem.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, product=item.product, defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        item.delete()
        return Response({'detail': 'Moved to cart.'})
