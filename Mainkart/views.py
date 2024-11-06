from django.shortcuts import render
from store.models import Product
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserSerializer, AuthTokenSerializer
from rest_framework.settings import api_settings
def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('-views')[:8]

    context = {
        'products': products,
    }
    return render(request, 'index.html', context)

class CreateTokenView(ObtainAuthToken):
    """ Create a new auth token for user """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Manage the authenticated user """
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """ Retrieve and return the authenticated user """
        return self.request.user
