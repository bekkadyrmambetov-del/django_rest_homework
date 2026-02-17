from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ProductWithReviewsSerializer






class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD для категорий
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD для товаров
    """
    queryset = Product.objects.prefetch_related('reviews')
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def reviews(self, request):
        products = self.get_queryset()
        serializer = ProductWithReviewsSerializer(products, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    CRUD для отзывов
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

