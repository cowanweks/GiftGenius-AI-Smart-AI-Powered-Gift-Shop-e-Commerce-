from rest_framework import serializers

from products.serializers import ProductSerializer


class GiftFinderRequestSerializer(serializers.Serializer):
    age = serializers.IntegerField(min_value=0, max_value=120)
    gender = serializers.ChoiceField(choices=['male', 'female', 'unisex', 'kids'])
    relationship = serializers.ChoiceField(
        choices=['partner', 'spouse', 'parent', 'sibling', 'friend', 'colleague', 'child']
    )
    occasion = serializers.ChoiceField(
        choices=[
            'birthday', 'anniversary', 'wedding', 'graduation', 'valentine',
            'christmas', 'mothers_day', 'fathers_day', 'baby_shower', 'general',
        ]
    )
    min_budget = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    max_budget = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)

    def validate(self, attrs):
        if attrs['min_budget'] > attrs['max_budget']:
            raise serializers.ValidationError('min_budget cannot be greater than max_budget.')
        return attrs


class GiftRecommendationSerializer(serializers.Serializer):
    product = ProductSerializer()
    score = serializers.IntegerField()
    reasons = serializers.ListField(child=serializers.CharField())
