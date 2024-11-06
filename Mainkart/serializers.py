from rest_framework import serializers
from accounts.models import Account
from django.contrib.auth import (
    authenticate
)
from django.utils.translation import gettext as _

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'phonenumber')

    def update(self, instance, validated_data):
        """ update and return user """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user

class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user auth token """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False,
    )
    def validate(self, attrs):
        """ Validate and authenticare the user """
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('password'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('wrong credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user']= user
        return attrs