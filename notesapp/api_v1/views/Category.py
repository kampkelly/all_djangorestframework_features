from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets, mixins, generics
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
    '''
    This class based view does not automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    But http methods such as get, post, put, delete, etc can be added.
    See mixins for methods that can be added here.
    '''
    throttle_classes = [UserThrottlePerMinute]
    def get(self, request, format=None):
        """
        Return a list of all categories.
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryListMixins(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    '''
    Using mixins for list and create.
    Simpler way of implementing http methods in `class CategoryAPIView(APIView):`
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryDetailMixins(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
    '''
    Using mixins for retrieve, update and delete.
    Simpler way of implementing http methods in `class CategoryAPIView(APIView):`
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CategoryListGenericApiView(generics.ListCreateAPIView):
    '''
    Even simpler way of implementing `class CategoryListMixins`.
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailGenericApiView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Even simpler way of implementing `class CategoryDetailMixins`.
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryView(ViewSet):
    '''
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions when the methods are created within the class.
    '''
    @method_decorator(cache_page(10)) # Cache requested url for each user for 30 minutes
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

    def retrieve(self, request, pk=None, format=None):
        '''
        Lists all categories.
        '''
        if request.version == 'api_v1':
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response('picking a particular object', status=status.HTTP_200_OK)
        else:
            WrongVersion.default_detail = 'Accessing wrong api version, use api_v1'
            raise WrongVersion

    @action(methods=['get'], detail=False, url_path='categories-list', url_name='my-lists')
    def categories_list(self, request, pk=None, format=None):
        '''
        This method demos router @action.

        It shows how to add an extra path to a ViewSet outside the default
        `list`, `create`, `retrieve`, `update` and `destroy` actions.
        '''
        if request.version == 'api_v1':
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response('serializer.data', status=status.HTTP_200_OK)
        else:
            WrongVersion.default_detail = 'Accessing wrong api version, use api_v1'
            raise WrongVersion



class CategoryViewSet(viewsets.ModelViewSet):
    '''
    Simpler way of implementing the `class CategoryView(ViewSet)`.

    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    There is no need to create list, retrieve etc. methods.
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryFunctionView:
    '''
    Function based views
    '''
    @api_view(['GET'])
    def list_categories(request, format=None):
        '''
        Function based view to list all categories.
        '''
        if request.version == 'api_v2':
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            WrongVersion.default_detail = 'Accessing wrong api version, use api_v2'
            raise WrongVersion
