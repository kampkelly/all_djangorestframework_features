
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination

from api_v1.models import Category, Notes
from api_v1.serializers import NotesModelSerializer

class NotesViewSet(ViewSet):
    '''
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions when the methods are created within the class.
    '''
    @method_decorator(cache_page(10)) # Cache requested url for each user for 30 minutes
    @method_decorator(vary_on_cookie)
    def list(self, request, format=None):
        notes = Notes.objects.all()
        serializer = NotesModelSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, format=None):
        print(request.data)
        serializer = NotesModelSerializer(data=request.data)
        print('>>>', NotesModelSerializer())
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except:
            return Response('internal server error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
