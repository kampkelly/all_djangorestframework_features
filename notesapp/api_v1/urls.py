from django.urls import path
from rest_framework import routers

from .views import Category

app_name = 'api_v1'

router = routers.SimpleRouter()

# function based views
list_categories = Category.CategoryFunctionView.list_categories

# class based views routes
router.register(r'categories', Category.CategoryView, 'categories-ViewSet')
router.register(r'cat', Category.CategoryViewSet, 'cat-viewsets')

urlpatterns = [
    # function based views urls
    path('fn/categories', list_categories, name='fn_categories'),

    # class based views
    # api views urls
    path('cls-apiviews/categories/', Category.CategoryAPIView.as_view(), name='apiviews_categories'),

    # mixins urls
    path('cls-mixins/categories/', Category.CategoryListMixins.as_view(), name='mixins_categories'),
    path('cls-mixins/categories/<int:pk>/', Category.CategoryDetailMixins.as_view(), name='mixins_categories'),

    # generic ApiViews urls
    path('cls-generics/categories/', Category.CategoryListGenericApiView.as_view(), name='generics_categories'),
    path('cls-generics/categories/<int:pk>/', Category.CategoryDetailGenericApiView.as_view(), name='generics_categories'),
]
urlpatterns += router.urls
