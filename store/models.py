from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.
#مدل محصولات
class Product(models.Model):
    product_name        = models.CharField(max_length=200,unique=True)
    product_slug        = models.SlugField(max_length=200,unique=True)
    product_description = models.TextField(max_length=500,blank=True)
    product_price       = models.FloatField()
    product_images      = models.ImageField(upload_to='photo/products')
    product_stock       = models.IntegerField()
    is_available        = models.BooleanField(default=True)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE) 
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

# برای گرفتن لینک محصول
    def get_url(self):
        return reverse('products_detail', args=[self.category.category_slug, self.product_slug])

variation_category_choice = (
    ('color', 'color'),
    ('size' , 'size'),
)

class Variations(models.Model):
    product            = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='variations')
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value    = models.CharField(max_length=100)
    is_active          = models.BooleanField(default=True)
    created_date       = models.DateField(auto_now=True)

    def __str__(self):
        return self.product.product_name




