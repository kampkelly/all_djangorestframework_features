from django.urls import path

from .views import Category

app_name = 'api_v1'

# function based views
list_categories = Category.CategoryFunctionView.list_categories

# class based views
categories = Category.CategoryView.as_view({
    'get': 'list'
})

urlpatterns = [
    # class based views urls
    path('categories', categories, name='categories'),
    # function based views urls
    path('fn/categories', list_categories, name='categories')
]
