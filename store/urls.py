from django.urls import path
from . import views
from .views import ProductView



urlpatterns = [
    path('products/', ProductView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductView.as_view(), name='product-detail-update'),
    path('', views.store, name='store'),
    path('search/', views.search, name='search'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>', views.product_detail, name='products_detail'),
    path('submit_review/<int:product_id>', views.submit_review, name='submit_review'),

]