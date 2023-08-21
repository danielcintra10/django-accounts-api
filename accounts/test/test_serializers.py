from django.test import TestCase
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from api.serializers import UserSerializer, MyTokenObtainPairSerializer
from accounts.models import User


class TestUserSerializer(TestCase):
    """Test UserSerializer to check if works properly"""

    def setUp(self):
        self.test_user = User.objects.create(email='robert@gmail.com',
                                             first_name='Robert',
                                             last_name='López Pérez',
                                             country='España',
                                             city='Barcelona',
                                             address='Barcelona España',
                                             mobile_phone='+34 10101023',
                                             password='PasswordStrong1234')

    def test_serialize_user_data_ok(self):
        user = User.objects.get(email__exact='robert@gmail.com')
        serializer = UserSerializer(user, many=False)
        self.assertEqual('Robert', serializer.data.get("first_name"))
        self.assertEqual('López Pérez', serializer.data.get("last_name"))
        self.assertEqual('robert@gmail.com', serializer.data.get("email"))
        self.assertEqual('España', serializer.data.get("country"))
        self.assertEqual('Barcelona', serializer.data.get("city"))
        self.assertEqual('Barcelona España', serializer.data.get("address"))
        self.assertEqual('+34 10101023', serializer.data.get("mobile_phone"))
        self.assertTrue("password" not in serializer.data)
        self.assertFalse(serializer.data.get("is_admin_user"))

    def test_deserialize_valid_user_object(self):
        serialized_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "country": "USA",
            "city": "New York",
            "address": "123 Main St",
            "mobile_phone": "+1 123456789",
            "password": "StrongPassword123",
        }
        serializer = UserSerializer(data=serialized_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "johndoe@example.com")
        self.assertEqual(user.country, "Usa")
        self.assertEqual(user.city, "New York")
        self.assertEqual(user.address, "123 Main St")
        self.assertEqual(user.mobile_phone, "+1 123456789")
        self.assertTrue(user.check_password("StrongPassword123"))
        self.assertFalse(user.is_staff)

    def test_update_valid_user_object(self):
        user = User.objects.get(email__exact='robert@gmail.com')
        updated_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "country": "USA",
            "city": "New York",
            "address": "123 Main St",
            "mobile_phone": "+1 123456789",
            "password": "StrongPassword123",
        }
        serializer = UserSerializer(instance=user, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "johndoe@example.com")
        self.assertEqual(user.country, "Usa")
        self.assertEqual(user.city, "New York")
        self.assertEqual(user.address, "123 Main St")
        self.assertEqual(user.mobile_phone, "+1 123456789")
        self.assertTrue(user.check_password("StrongPassword123"))
        self.assertFalse(user.is_staff)

    def test_validation_error_non_unique_email(self):
        user_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "robert@gmail.com",
            "country": "Canada",
            "city": "Toronto",
            "address": "456 Maple Ave",
            "mobile_phone": "+0 9876543210",
            "password": "NewPassword456",
        }
        serializer = UserSerializer(data=user_data)
        self.assertFalse(serializer.is_valid())

    def test_validation_error_non_unique_mobile_phone(self):
        user_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "janesmith@example.com",
            "country": "Canada",
            "city": "Toronto",
            "address": "456 Maple Ave",
            "mobile_phone": "+34 10101023",
            "password": "NewPassword456",
        }
        serializer = UserSerializer(data=user_data)
        self.assertFalse(serializer.is_valid())

    def test_validation_error_weak_password(self):
        user_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "janesmith@example.com",
            "country": "Canada",
            "city": "Toronto",
            "address": "456 Maple Ave",
            "mobile_phone": "+1 0000000000",
            "password": "1234",
        }
        serializer = UserSerializer(data=user_data)
        self.assertFalse(serializer.is_valid())

    def test_read_only_id_and_is_admin_user_fields_are_ok_when_serialize(self):
        user = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            country="USA",
            city="New York",
            address="123 Main St",
            mobile_phone="1234567890",
            password="StrongPassword123",
        )
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data["id"], user.id)
        self.assertEqual(serializer.data["is_admin_user"], user.is_staff)

    def test_read_only_id_and_is_admin_user_fields_not_when_deserialize(self):
        user_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "janesmith@example.com",
            "country": "Canada",
            "city": "Toronto",
            "address": "456 Maple Ave",
            "mobile_phone": "+1 0000000000",
            "password": "StrongPassword1234",
        }
        serializer = UserSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        with self.assertRaises(KeyError):
            id = serializer.validated_data["id"]
            is_admin_user = serializer.validated_data["is_admin_user"]

    def test_save_user_object_with_correct_fields(self):
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "country": "USA",
            "city": "New York",
            "address": "123 Main St",
            "mobile_phone": "+0 1234567890",
            "password": "StrongPassword123",
        }
        serializer = UserSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        user = User.objects.get(email__exact="johndoe@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "johndoe@example.com")
        self.assertEqual(user.country, "Usa")
        self.assertEqual(user.city, "New York")
        self.assertEqual(user.address, "123 Main St")
        self.assertEqual(user.mobile_phone, "+0 1234567890")
        self.assertTrue(user.check_password("StrongPassword123"))
        self.assertFalse(user.is_staff)


class TestMyTokenObtainPairSerializer(TestCase):
    """Test MyTokenObtainPairSerializer to check if works properly"""

    def setUp(self):
        self.test_user = User.objects.create(email='robert@gmail.com',
                                             first_name='Robert',
                                             last_name='López Pérez',
                                             country='España',
                                             city='Barcelona',
                                             address='Barcelona España',
                                             mobile_phone='+34 10101023',
                                             password='PasswordStrong1234')

    def test_validate_method_returns_expected_data_representation(self):
        serializer = MyTokenObtainPairSerializer()
        attrs = {'email': 'robert@gmail.com', 'password': 'PasswordStrong1234'}

        result = serializer.validate(attrs)

        assert 'user' in result
        assert 'access_token' in result
        assert 'refresh_token' in result
        assert 'token_type' in result
        assert result['token_type'] == 'Bearer'

    def test_invalid_credentials_raise_authenticationfailed_error(self):
        serializer = MyTokenObtainPairSerializer()
        attrs = {'email': 'invaliduser', 'password': 'invalidpassword'}

        with self.assertRaises(AuthenticationFailed):
            serializer.validate(attrs)

    def test_missing_credentials_raise_key_error(self):
        serializer = MyTokenObtainPairSerializer()
        attrs = {}

        with self.assertRaises(KeyError):
            serializer.validate(attrs)

    def test_user_object_correctly_serialized_in_data_representation(self):
        serializer = MyTokenObtainPairSerializer()
        attrs = {'email': 'robert@gmail.com', 'password': 'PasswordStrong1234'}

        result = serializer.validate(attrs)

        assert 'user' in result
        assert 'id' in result['user']
        assert 'first_name' in result['user']
        assert 'last_name' in result['user']
        assert 'email' in result['user']
        assert 'mobile_phone' in result['user']
        assert 'country' in result['user']
        assert 'city' in result['user']
        assert 'address' in result['user']
        assert 'is_admin_user' in result['user']

    def test_correct_data_in_serializer_data(self):
        serializer = MyTokenObtainPairSerializer()
        attrs = {'email': 'robert@gmail.com', 'password': 'PasswordStrong1234'}

        data = serializer.validate(attrs)
        self.assertEqual(data.get("user").get("first_name"), "Robert")
        self.assertEqual(data.get("user").get("last_name"), "López Pérez")
        self.assertEqual(data.get("user").get("email"), "robert@gmail.com")
        self.assertEqual(data.get("user").get("country"), "España")
        self.assertEqual(data.get("user").get("city"), "Barcelona")
        self.assertEqual(data.get("user").get("address"), "Barcelona España")
        self.assertEqual(data.get("user").get("mobile_phone"), "+34 10101023")
        self.assertEqual(data.get("user").get("is_admin_user"), False)
        self.assertEqual(data.get("token_type"), "Bearer")
