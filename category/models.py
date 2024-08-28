from django.db import models
from django.urls import reverse
# Create your models here.
#مدل کاتگوری
class Category (models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    category_slug = models.SlugField(max_length=150, unique=True)
    category_description = models.TextField(max_length=255, blank=True)
    category_image = models.ImageField(upload_to='photo/categories', blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
#فانکشن برای گرفتن لینک
    def get_url(self):
        return reverse('products_by_category', args=[self.category_slug])


    def __str__(self):
        return self.category_name