from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from api_v1.models import Category
from api_v1.serializers import CategorySerializer


class CategoryView(ViewSet):
    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryFunctionView:
    @api_view(['GET'])
    def list_categories(request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
