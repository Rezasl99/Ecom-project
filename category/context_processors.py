from .models import Category


# گلوبال کاتگوری
def Category_links(request):
    category_links = Category.objects.all()
    return dict(category_links=category_links)