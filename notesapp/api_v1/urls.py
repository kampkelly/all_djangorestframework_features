from django.urls import path

from .views import Category

app_name = 'api_v1'

categories = Category.CategoryView.as_view({
    'get': 'list'
})

urlpatterns = [
    path('categories', categories, name='categories')
]