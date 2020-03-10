from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.decorators import action

from api_v1.models import Category
from api_v1.serializers import CategorySerializer
from api_v1.helpers.throttles import UserThrottlePerMinute


class WrongVersion(APIException):
    status_code = 400
    default_detail = 'Accessing wrong api version'
    default_code = 'wrong_api_version'


class CategoryAPIView(APIView):
    throttle_classes = [UserThrottlePerMinute]
    def get(self, request, format=None):
        """
        Return a list of all categories.
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryView(ViewSet):
    # Cache requested url for each user for 30 minutes
    @method_decorator(cache_page(1800))
    @method_decorator(vary_on_cookie)
    def list(self, request, format=None):
        '''
        Lists all categories.
        '''
        if request.version == 'api_v1':
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            WrongVersion.default_detail = 'Accessing wrong api version, use api_v1'
            raise WrongVersion

    @action(methods=['get'], detail=False, url_path='categories-list', url_name='my-lists')
    def categories_list(self, request, pk=None, format=None):
        '''
        This method is just to demo router @action.
        '''
        if request.version == 'api_v1':
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response('serializer.data', status=status.HTTP_200_OK)
        else:
            WrongVersion.default_detail = 'Accessing wrong api version, use api_v1'
            raise WrongVersion


class CategoryFunctionView:
    @api_view(['GET'])
    def list_categories(request, format=None):
        '''
        Lists all categories.
        '''
        if request.version == 'api_v2':
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            WrongVersion.default_detail = 'Accessing wrong api version, use api_v2'
            raise WrongVersion
