from django.contrib import admin
from django.urls import path , include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/',SpectacularSwaggerView.as_view(url_name='api-schema'),  name='api-docs'),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('notadmin/', admin.site.urls),
    path('' ,views.home , name='home'),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
