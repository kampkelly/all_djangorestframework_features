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
from rest_framework.pagination import PageNumberPagination, CursorPagination

from api_v1.models import Category
from api_v1.serializers import CategoryModelSerializer, CategorySerializer
from api_v1.helpers.throttles import UserThrottlePerMinute


class WrongVersion(APIException):
    status_code = 400
    default_detail = 'Accessing wrong api version'
    default_code = 'wrong_api_version'


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })

class StandardCursorPagination(CursorPagination):
    '''
    This pagination requires that there is a unique, unchanging ordering of items in the result set.
    This ordering might typically be a creation timestamp on the records, as this presents a 
    consistent ordering to paginate against
    '''
    page_size = 2
    ordering ='created_at'
    page_query_param = 'page'
    max_page_size = 10


class CategoryAPIView(APIView):
    '''
    This class based view does not automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    But http methods such as get, post, put, delete, etc can be added.
    See mixins for methods that can be added here.
    '''
    pagination_class = StandardResultsSetPagination
    throttle_classes = [UserThrottlePerMinute]
    def get(self, request, format=None):
        """
        Return a list of all categories.
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = {'name':request.data['name']}
        serializer = CategorySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except:
            return Response('An error occured', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def get(self, request, pk=None, format=None): # for detail
    #     category = Category.objects.get(pk=1)
    #     if category:
    #         serializer = CategorySerializer(category)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response('category not found', status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk=None, format=None):
        data = {'name':request.data['name']}
        category = Category.objects.get(pk=pk)
        if category:
            serializer = CategorySerializer(category, data=data)
            if serializer.is_valid():
                try:
                    serializer.save()
                except:
                    return Response('An error occured', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('category not found', status=status.HTTP_404_NOT_FOUND)


class CategoryListMixins(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    '''
    Using mixins for list and create.
    Simpler way of implementing http methods in `class CategoryAPIView(APIView):`
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardCursorPagination

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
    serializer_class = CategoryModelSerializer
    pagination_class = StandardResultsSetPagination


class CategoryDetailGenericApiView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Even simpler way of implementing `class CategoryDetailMixins`.
    '''
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


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
            serializer = CategoryModelSerializer(categories, many=True)
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
            serializer = CategoryModelSerializer(categories, many=True)
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
            serializer = CategoryModelSerializer(categories, many=True)
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
            serializer = CategoryModelSerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            WrongVersion.default_detail = 'Accessing wrong api version, use api_v2'
            raise WrongVersion
