from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import APIException

from api_v1.models import Category
from api_v1.serializers import CategorySerializer


class WrongVersion(APIException):
    status_code = 400
    default_detail = 'Accessing wrong api version'
    default_code = 'wrong_api_version'


class CategoryView(ViewSet):
    def list(self, request, format=None):
        if request.version == 'api_v1':
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            WrongVersion.default_detail = 'Accessing wrong api version, use api_v1'
            raise WrongVersion


class CategoryFunctionView:
    @api_view(['GET'])
    def list_categories(request, format=None):
        if request.version == 'api_v2':
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            WrongVersion.default_detail = 'Accessing wrong api version, use api_v2'
            raise WrongVersion
