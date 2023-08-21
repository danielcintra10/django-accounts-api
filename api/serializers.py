from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    is_admin_user = serializers.BooleanField(source='is_staff', read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name", "last_name",
            "email", "country",
            "city", "address",
            "mobile_phone", "password",
            "is_admin_user",
        )
        read_only_fields = ("id",)
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, password):
        validate_password(password)
        return password


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    token_type = 'Bearer'

    def validate(self, attrs):
        data = super().validate(attrs)
        new_data_representation = {
            'user': {'id': self.user.id,
                     'first_name': self.user.first_name,
                     'last_name': self.user.last_name,
                     'email': self.user.email,
                     'mobile_phone': self.user.mobile_phone,
                     'country': self.user.country,
                     'city': self.user.city,
                     'address': self.user.address,
                     'is_admin_user': self.user.is_staff},
            'access_token': data['access'],
            'refresh_token': data['refresh'],
            'token_type': self.token_type
        }
        return new_data_representation
