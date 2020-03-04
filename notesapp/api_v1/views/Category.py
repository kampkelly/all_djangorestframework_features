from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from api_v1.models import Category
# from api.serializers import CategorySerializer, save_serializer


class CategoryView(ViewSet):
    def list(self, request):
        categories = Category.objects.all()
        # serializer = CategorySerializer(categories, many=True)
        return Response(categories, status=status.HTTP_200_OK)
