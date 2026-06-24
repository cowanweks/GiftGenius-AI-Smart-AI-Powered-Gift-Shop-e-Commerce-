from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .engine import recommend_gifts
from .serializers import GiftFinderRequestSerializer, GiftRecommendationSerializer


class GiftFinderView(APIView):
    """POST /api/recommendations/gift-finder/

    Accepts recipient details (age, gender, relationship, occasion, budget)
    and returns AI-style ranked gift suggestions from the rule-based engine.
    A real OpenAI integration could replace `recommend_gifts` without
    changing this view's contract.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        request_serializer = GiftFinderRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        data = request_serializer.validated_data

        results = recommend_gifts(
            age=data['age'],
            gender=data['gender'],
            relationship=data['relationship'],
            occasion=data['occasion'],
            min_budget=data['min_budget'],
            max_budget=data['max_budget'],
        )

        response_serializer = GiftRecommendationSerializer(
            results, many=True, context={'request': request}
        )
        return Response({'count': len(results), 'recommendations': response_serializer.data})
