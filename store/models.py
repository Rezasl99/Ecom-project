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
    category            = models.ForeignKey(Category, on_delete=models.CASCADE) #با استفاده از کاتگوری به عنوان فارن کی
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

#اینم برای گرفتن لینک محصول
    def get_url(self):
        return reverse('products_detail', args=[self.category.category_slug, self.product_slug])





