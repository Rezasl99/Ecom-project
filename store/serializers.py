from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    average_review = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'product_name',
            'product_fa_name',
            'product_slug',
            'product_description',
            'product_price',
            'product_images',
            'product_stock',
            'is_available',
            'category',
            'created_date',
            'modified_date',
            'views',
            'average_review',
            'review_count',
            'name',
            'url'
        ]

    def get_average_review(self, obj):
        return obj.averageReview()

    def get_review_count(self, obj):
        return obj.countReview()

    def get_name(self, obj):
        return obj.get_name()

    def get_url(self, obj):
        return obj.get_url()
