from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from api_v1.models import Category
from api_v1.serializers import CategorySerializer

class CategoryView(ViewSet):
    def list(self, request):
        if request.version == 'api_v1':
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = "use api_v1"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class CategoryFunctionView:
    @api_view(['GET'])
    def list_categories(request):
        if request.version == 'api_v2':
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = "use api_v2"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)