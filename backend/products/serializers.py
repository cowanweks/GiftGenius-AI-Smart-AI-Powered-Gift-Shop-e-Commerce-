from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'icon')


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'description', 'price', 'category', 'category_name',
            'occasion', 'gender', 'stock', 'image', 'rating', 'rating_count',
            'is_trending', 'is_featured', 'min_age', 'max_age', 'created_at',
        )

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return obj.image_url or None


class ProductWriteSerializer(serializers.ModelSerializer):
    """Used by the admin dashboard to create/update products."""

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'description', 'price', 'category',
            'occasion', 'gender', 'stock', 'image', 'image_url', 'rating',
            'rating_count', 'is_trending', 'is_featured', 'min_age', 'max_age',
        )
