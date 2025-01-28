from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import create_request, AvailableProductListView, ProfessorListView, CategoryListAPIView

urlpatterns = [
    path('create-request/', create_request, name='create-request'),
    path('available-products/', AvailableProductListView.as_view(), name='available-products'),
    path('professors/', ProfessorListView.as_view(), name='professor-list'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),

]