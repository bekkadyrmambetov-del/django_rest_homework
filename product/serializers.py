from rest_framework import serializers
from django.db.models import Avg
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']
        read_only_fields = ['products_count']

    products_count = serializers.SerializerMethodField()

    def get_products_count(self, obj):
        return obj.products.count()


    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название категории не может быть пустым")
        return value


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название товара не может быть пустым")
        return value


    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("Описание товара не может быть пустым")
        return value

    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена товара должна быть больше 0")
        return value


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

    
    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Текст отзыва не может быть пустым")
        return value


    def validate_stars(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5")
        return value


    def validate_product(self, value):
        if not value:
            raise serializers.ValidationError("Товар должен существовать")
        return value


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'rating']

    def get_rating(self, obj):
        return obj.reviews.aggregate(avg=Avg('stars'))['avg']















# from rest_framework import serializers
# from django.db.models import Avg
# from .models import Category, Product, Review



# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = '__all__'
        



# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'






# class ProductWithReviewsSerializer(serializers.ModelSerializer):
#     reviews = ReviewSerializer(many=True, read_only=True)
#     rating = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'rating']

#     def get_rating(self, obj):
#         return obj.reviews.aggregate(avg=Avg('stars'))['avg']



# class CategorySerializer(serializers.ModelSerializer):
#     products_count = serializers.SerializerMethodField()

#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'products_count']

#     def get_products_count(self, obj):
#         return obj.products.count()