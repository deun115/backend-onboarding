from django.urls import path
from boards import views
from boards.views import CategoryCreateAPIView, CategoryListAPIView

urlpatterns = [
    path('', CategoryListAPIView.as_view(), name='category_list'),
    path('category-create/', CategoryCreateAPIView.as_view(), name='category_create')
]
