from django.urls import path
from rest_framework import routers

from .views import Category

app_name = 'api_v1'

router = routers.SimpleRouter()

# function based views
list_categories = Category.CategoryFunctionView.list_categories

router.register(r'categories', Category.CategoryView, 'categories')

urlpatterns = [
    # function based views urls
    path('fn/categories', list_categories, name='categories')
]
urlpatterns += router.urls
