from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count
from django.utils import timezone
from django.utils import translation
# Create your models here.
#مدل محصولات
class Product(models.Model):
    product_name        = models.CharField(max_length=200,unique=True)
    product_fa_name     = models.CharField(max_length=100, default='نام محصول')
    product_slug        = models.SlugField(max_length=200,unique=True)
    product_description = models.TextField(max_length=500,blank=True)
    product_price       = models.FloatField()
    product_images      = models.ImageField(upload_to='photo/products')
    product_stock       = models.IntegerField()
    is_available        = models.BooleanField(default=True)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)
    views               = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def get_name(self):
        if translation.get_language() == 'fa':
            return self.product_fa_name
        return self.product_name
#
    def get_url(self):
        """ Helper function for getting the url of the product """
        return reverse('products_detail', args=[self.category.category_slug, self.product_slug])

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

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

    objects = VariationManager()
    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(blank=True, max_length=100)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    ip  = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class ProductView(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=45)  # IPv6-compatible
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('product', 'ip_address')  # Each IP can only have one record per product

    def __str__(self):
        return f"{self.product} viewed by {self.ip_address}"


