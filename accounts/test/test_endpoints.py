from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from collections import OrderedDict


class TestListCreateUser(APITestCase):
    """Test /api/v1/accounts/users/ endpoint, check responses, permissions and constraints"""

    def setUp(self):
        self.test_user = User.objects.create_superuser(email='robert@gmail.com',
                                                       first_name='Robert',
                                                       last_name='López Pérez',
                                                       country='España',
                                                       city='Barcelona',
                                                       address='Barcelona España',
                                                       mobile_phone='+34 10101023',
                                                       password='PasswordStrong1234')

        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_get_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.get('/api/v1/accounts/users/')
        self.assertEqual(response.status_code, 401)

    def test_post_request_create_user_with_valid_data_returns_201(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "country": "USA",
            "city": "New York",
            "address": "123 Main St",
            "mobile_phone": "+1 123456789",
            "password": "StrongPassword123",
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 201)

    def test_post_request_create_user_with_valid_data_from_spanish_keyboard_returns_201(self):
        data = {
            "first_name": "José",
            "last_name": "Gómez",
            "email": "jose@example.com",
            "country": "España",
            "city": "Cádiz",
            "address": "123 Main St",
            "mobile_phone": "+1 123456789",
            "password": "StrongPassword123",
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 201)

    def test_post_request_create_correct_new_user_db_count_equal_2(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "country": "USA",
            "city": "New York",
            "address": "123 Main St",
            "mobile_phone": "+1 123456789",
            "password": "StrongPassword123",
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)

    def test_post_request_return_correct_data(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "country": "USA",
            "city": "New York",
            "address": "123 Main St",
            "mobile_phone": "+1 123456789",
            "password": "StrongPassword123",
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)
        user = User.objects.get(email__exact="johndoe@example.com")
        self.assertEqual(response.data, {'id': user.id,
                                         'first_name': user.first_name,
                                         'last_name': user.last_name,
                                         'email': user.email,
                                         'country': user.country,
                                         'city': user.city,
                                         'address': user.address,
                                         'mobile_phone': user.mobile_phone,
                                         'is_admin_user': user.is_staff,
                                         })

    def test_upper_camel_case_names_method(self):
        data = {
            "first_name": "JOHN",
            "last_name": "doE",
            "email": "johndoe@example.com",
            "country": "USA",
            "city": "NEW york",
            "address": "123 Main St",
            "mobile_phone": "+1 123456789",
            "password": "StrongPassword123",
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        user = User.objects.get(email__exact="johndoe@example.com")
        self.assertEqual(response.data, {'id': user.id,
                                         'first_name': 'John',
                                         'last_name': 'Doe',
                                         'email': user.email,
                                         'country': 'Usa',
                                         'city': 'New York',
                                         'address': user.address,
                                         'mobile_phone': user.mobile_phone,
                                         'is_admin_user': user.is_staff,
                                         })

    def test_post_request_validate_email_unique_constraint(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "robert@gmail.com",
            "country": "USA",
            "city": "New York",
            "address": "123 Main St",
            "mobile_phone": "+1 123456789",
            "password": "StrongPassword123",
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_validate_mobile_phone_unique_constraint(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "country": "USA",
            "city": "New York",
            "address": "123 Main St",
            "mobile_phone": "+34 10101023",
            "password": "StrongPassword123",
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_validate_secure_password(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "country": "USA",
            "city": "New York",
            "address": "123 Main St",
            "mobile_phone": "+001 103101023",
            "password": "1234",
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_returns_400_when_create_users_with_wrong_email(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "email",
            "country": "USA",
            "city": "New York",
            "address": "123 Main St",
            "mobile_phone": "+1 1000101023",
            "password": "StrongPassword123",
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_returns_400_when_create_users_with_wrong_first_name(self):
        data = {
            "first_name": "John23@ #1",
            "last_name": "Doe",
            "email": "example@mail.com",
            "country": "USA",
            "city": "New York",
            "address": "123 Main St",
            "mobile_phone": "+1 1000101023",
            "password": "StrongPassword123",
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_returns_400_when_create_users_with_wrong_last_name(self):
        data = {
            "first_name": "John",
            "last_name": "Doe 45@#*(",
            "email": "example@mail.com",
            "country": "USA",
            "city": "New York",
            "address": "123 Main St",
            "mobile_phone": "+1 1000101023",
            "password": "StrongPassword123",
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_returns_400_when_create_users_with_wrong_country_name(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "country": "23**USA",
            "city": "New York",
            "address": "123 Main St",
            "mobile_phone": "+1 1000101023",
            "password": "StrongPassword123",
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_returns_400_when_create_users_with_wrong_city_name(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "country": "USA",
            "city": "New   4   York",
            "address": "123 Main St",
            "mobile_phone": "+1 1000101023",
            "password": "StrongPassword123",
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_returns_400_when_create_users_with_wrong_mobile_phone_format(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "country": "USA",
            "city": "New York",
            "address": "123 Main St",
            "mobile_phone": "1000101023",
            "password": "StrongPassword123",
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_request_returns_400_when_create_users_with_non_numeric_characters_in_mobile_phone(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@mail.com",
            "country": "USA",
            "city": "New York",
            "address": "123 Main St",
            "mobile_phone": "+1 1000gdra1023",
            "password": "StrongPassword123",
        }
        self.client = APIClient()
        response = self.client.post('/api/v1/accounts/users/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_get_request_returns_200(self):
        response = self.client.get('/api/v1/accounts/users/')
        self.assertEqual(response.status_code, 200)

    def test_get_request_return_correct_data(self):
        response = self.client.get('/api/v1/accounts/users/')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data, [OrderedDict({'id': self.test_user.id,
                                                      'first_name': self.test_user.first_name,
                                                      'last_name': self.test_user.last_name,
                                                      'email': self.test_user.email,
                                                      'country': self.test_user.country,
                                                      'city': self.test_user.city,
                                                      'address': self.test_user.address,
                                                      'mobile_phone': self.test_user.mobile_phone,
                                                      'is_admin_user': self.test_user.is_staff,
                                                      })])


class TestRetrieveUpdateDestroyUser(APITestCase):
    """Test /api/v1/accounts/users/{id_user} endpoint, check responses and permissions"""

    def setUp(self):
        self.test_user = User.objects.create(id=1,
                                             email='robert@gmail.com',
                                             first_name='Robert',
                                             last_name='López Pérez',
                                             country='España',
                                             city='Barcelona',
                                             address='Barcelona España',
                                             mobile_phone='+34 10101023',
                                             password='PasswordStrong1234')
        self.test_admin_user = User.objects.create(id=2,
                                                   email='rossi@gmail.com',
                                                   first_name='Rossi',
                                                   last_name='Valentina',
                                                   country='Italia',
                                                   city='Milan',
                                                   address='Milan Italia',
                                                   mobile_phone='+55 101017890',
                                                   password='PasswordStrong1234',
                                                   is_staff=True,
                                                   is_superuser=False, )
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_get_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.get('/api/v1/accounts/users/1')
        self.assertEqual(response.status_code, 401)

    def test_get_request_access_authenticated_non_admin_user_returns_200(self):
        response = self.client.get('/api/v1/accounts/users/1')
        self.assertEqual(response.status_code, 200)

    def test_get_request_access_authenticated_non_admin_user_returns_403(self):
        """Test that a non-administrator user is not able to access other users than his own"""
        response = self.client.get('/api/v1/accounts/users/2')
        self.assertEqual(response.status_code, 403)

    def test_get_request_access_authenticated_admin_user_returns_200(self):
        """Test that an administrator user is able to access all users"""
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.test_admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        response = self.client.get('/api/v1/accounts/users/1')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1/accounts/users/2')
        self.assertEqual(response.status_code, 200)

    def test_get_request_return_correct_data(self):
        response = response = self.client.get('/api/v1/accounts/users/1')
        user = User.objects.get(email__exact="robert@gmail.com")
        self.assertEqual(response.data, {'id': user.id,
                                         'first_name': user.first_name,
                                         'last_name': user.last_name,
                                         'email': user.email,
                                         'country': user.country,
                                         'city': user.city,
                                         'address': user.address,
                                         'mobile_phone': user.mobile_phone,
                                         'is_admin_user': user.is_staff,
                                         })

    def test_put_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        # first_name, mobile_phone fields are updated
        data = {
            "first_name": "Robertico JR",
            "last_name": "López Pérez",
            "email": "robert@gmail.com",
            "country": "España",
            "city": "Barcelona",
            "address": "Barcelona España",
            "mobile_phone": "+34 99999999",
            "password": "StrongPassword1234",
        }
        response = response = self.client.put('/api/v1/accounts/users/1', data=data)
        self.assertEqual(response.status_code, 401)

    def test_put_request_access_authenticated_non_admin_user_returns_403(self):
        # first_name, mobile_phone fields are updated
        data = {
            "first_name": "Robertico JR",
            "last_name": "López Pérez",
            "email": "robert@gmail.com",
            "country": "España",
            "city": "Barcelona",
            "address": "Barcelona España",
            "mobile_phone": "+34 99999999",
            "password": "StrongPassword1234",
        }
        response = response = self.client.put('/api/v1/accounts/users/2', data=data)
        self.assertEqual(response.status_code, 403)

    def test_put_request_returns_200(self):
        # first_name, mobile_phone fields are updated
        data = {
            "first_name": "Robertico JR",
            "last_name": "López Pérez",
            "email": "robert@gmail.com",
            "country": "España",
            "city": "Barcelona",
            "address": "Barcelona España",
            "mobile_phone": "+34 99999999",
            "password": "StrongPassword1234",
        }
        response = response = self.client.put('/api/v1/accounts/users/1', data=data)
        user = User.objects.get(email__exact="robert@gmail.com")
        self.assertEqual(response.data, {'id': user.id,
                                         'first_name': user.first_name,
                                         'last_name': user.last_name,
                                         'email': user.email,
                                         'country': user.country,
                                         'city': user.city,
                                         'address': user.address,
                                         'mobile_phone': user.mobile_phone,
                                         'is_admin_user': user.is_staff,
                                         })
    def test_patch_request_access_unauthenticated_user_returns_401(self):
        self.client = APIClient()
        response = self.client.patch('/api/v1/accounts/users/1')
        self.assertEqual(response.status_code, 401)

    def test_patch_request_returns_200(self):
        # address, field is updated
        data = {
            "address": "Madrid España",
        }
        response = response = self.client.patch('/api/v1/accounts/users/1', data=data)
        user = User.objects.get(email__exact="robert@gmail.com")
        self.assertEqual(response.data, {'id': user.id,
                                         'first_name': user.first_name,
                                         'last_name': user.last_name,
                                         'email': user.email,
                                         'country': user.country,
                                         'city': user.city,
                                         'address': user.address,
                                         'mobile_phone': user.mobile_phone,
                                         'is_admin_user': user.is_staff,
                                         })


class TestLoginUser(APITestCase):
    """Test /api/v1/accounts/users/login endpoint, check responses and correct login credentials"""

    def setUp(self):
        self.test_user = User.objects.create(email='robert@gmail.com',
                                             first_name='Robert',
                                             last_name='López Pérez',
                                             country='España',
                                             city='Barcelona',
                                             address='Barcelona España',
                                             mobile_phone='+34 10101023',
                                             password='PasswordStrong1234')

        self.client = APIClient()

    def test_post_request_with_valid_data_return_200(self):
        data = {
            "email": "robert@gmail.com",
            "password": "PasswordStrong1234"
        }
        response = self.client.post('/api/v1/accounts/users/login', data=data)
        self.assertEqual(response.status_code, 200)

    def test_post_request_return_correct_data(self):
        data = {
            "email": "robert@gmail.com",
            "password": "PasswordStrong1234"
        }
        response = self.client.post('/api/v1/accounts/users/login', data=data)
        self.assertEqual(response.data, {
            'user': {
                'id': self.test_user.id,
                'first_name': self.test_user.first_name,
                'last_name': self.test_user.last_name,
                'email': self.test_user.email,
                'mobile_phone': self.test_user.mobile_phone,
                'country': self.test_user.country,
                'city': self.test_user.city,
                'address': self.test_user.address,
                'is_admin_user': self.test_user.is_staff
            },
            'access_token': response.data.get('access_token'),
            'refresh_token': response.data.get('refresh_token'),
            'token_type': 'Bearer'
        })

    def test_post_request_invalid_user_credentials_email(self):
        data = {
            "email": "wrongemail@gmail.com",
            "password": "PasswordStrong1234"
        }
        response = self.client.post('/api/v1/accounts/users/login', data=data)
        self.assertEqual(response.status_code, 401)

    def test_post_request_invalid_user_credentials_password(self):
        data = {
            "email": "robert@gmail.com",
            "password": "wrongpassword"
        }
        response = self.client.post('/api/v1/accounts/users/login', data=data)
        self.assertEqual(response.status_code, 401)
