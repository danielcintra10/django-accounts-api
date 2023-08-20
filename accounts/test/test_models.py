from django.core.exceptions import ValidationError
from django.test import TestCase
from accounts.models import User
from django.db.utils import IntegrityError


class TestUser(TestCase):
    """Test User model to check work properly"""

    def setUp(self):
        self.test_user = User.objects.create(email='robert@gmail.com',
                                             first_name='Robert',
                                             last_name='Lopez',
                                             country='Cuba',
                                             city='La Habana',
                                             address='Habana Cuba',
                                             mobile_phone='+53 59876543',
                                             password='1234')

    def test_create_new_user_with_valid_data(self):
        new_user = User.objects.create(email='migue@gmail.com',
                                       first_name='Miguel',
                                       last_name='Perez',
                                       country='Cuba',
                                       city='La Habana',
                                       address='Habana Cuba',
                                       mobile_phone='+53 51234567',
                                       password='password123')
        user = User.objects.filter(email__exact='migue@gmail.com').first()
        data = {'email': 'migue@gmail.com',
                'first_name': 'Miguel',
                'last_name': 'Perez',
                'country': 'Cuba',
                'city': 'La Habana',
                'address': 'Habana Cuba',
                'mobile_phone': '+53 51234567',
                'is_active': True,
                'is_staff': False,
                'is_superuser': False,
                }
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(data, {'email': user.email,
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'country': user.country,
                                'city': user.city,
                                'address': user.address,
                                'mobile_phone': user.mobile_phone,
                                'is_active': user.is_active,
                                'is_staff': user.is_staff,
                                'is_superuser': user.is_superuser,
                                })

    def test_create_new_superuser_with_valid_data(self):
        new_superuser = User.objects.create_superuser(email='kevin@gmail.com',
                                                      first_name='Kevin',
                                                      last_name='Gonzales',
                                                      country='Cuba',
                                                      city='La Habana',
                                                      address='Habana Cuba',
                                                      mobile_phone='+53 51234568',
                                                      username='kevin',
                                                      password='password123')

        superuser = User.objects.filter(email__exact='kevin@gmail.com').first()
        data = {'email': 'kevin@gmail.com',
                'first_name': 'Kevin',
                'last_name': 'Gonzales',
                'country': 'Cuba',
                'city': 'La Habana',
                'address': 'Habana Cuba',
                'mobile_phone': '+53 51234568',
                'is_active': True,
                'is_staff': True,
                'is_superuser': True,
                }
        self.assertEqual(User.objects.count(), 2)
        assert superuser.check_password('password123') is True
        self.assertEqual(data, {'email': superuser.email,
                                'first_name': superuser.first_name,
                                'last_name': superuser.last_name,
                                'country': superuser.country,
                                'city': superuser.city,
                                'address': superuser.address,
                                'mobile_phone': superuser.mobile_phone,
                                'is_active': superuser.is_active,
                                'is_staff': superuser.is_staff,
                                'is_superuser': superuser.is_superuser,
                                })

    def test_password_is_correct_encrypted(self):
        user = User.objects.filter(email__exact='robert@gmail.com').first()
        assert user.check_password('1234') is True

    def test_error_when_create_a_user_with_missing_fields(self):
        with self.assertRaises(Exception):
            new_user = User.objects.create(email='migue@gmail.com',
                                           first_name='Miguel',
                                           last_name='Perez',
                                           )

    def test_update_user_with_valid_data(self):
        user = User.objects.filter(email__exact='robert@gmail.com').first()
        user.first_name = 'Jose'
        user.last_name = 'Hernandez Gomez'
        user.email = 'jose@gmail.com'
        user.mobile_phone = '+34 10101023'
        user.country = 'España'
        user.city = 'Barcelona'
        user.save()
        data = {'email': 'jose@gmail.com',
                'first_name': 'Jose',
                'last_name': 'Hernandez Gomez',
                'country': 'España',
                'city': 'Barcelona',
                'address': 'Habana Cuba',
                'mobile_phone': '+34 10101023',
                'is_active': True,
                'is_staff': False,
                'is_superuser': False,
                }
        self.assertEqual(data, {'email': user.email,
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'country': user.country,
                                'city': user.city,
                                'address': user.address,
                                'mobile_phone': user.mobile_phone,
                                'is_active': user.is_active,
                                'is_staff': user.is_staff,
                                'is_superuser': user.is_superuser,
                                })

    def test_delete_user(self):
        new_user = User.objects.create(email='migue@gmail.com',
                                       first_name='Miguel',
                                       last_name='Perez',
                                       country='Cuba',
                                       city='La Habana',
                                       address='Habana Cuba',
                                       mobile_phone='+53 51234567',
                                       password='password123')
        self.assertEqual(User.objects.count(), 2)
        new_user.delete()
        self.assertEqual(User.objects.count(), 1)
        self.assertFalse(User.objects.filter(email__exact='migue@gmail.com').exists())

    def test_username_field_equal_to_first_name(self):
        new_user = User.objects.create(email='email@gmail.com',
                                       first_name='First Name',
                                       last_name='Last Name',
                                       country='Country',
                                       city='City',
                                       address='Address',
                                       mobile_phone='+000 12345698',
                                       password='password123')
        self.assertEqual('First Name', new_user.username)

    def test_database_return_correct_user_looking_for_email_field(self):
        user = User.objects.filter(email__exact='robert@gmail.com').first()
        self.assertEqual(user, self.test_user)

    def test_user_can_update_password(self):
        self.test_user.password = 'password123'
        self.test_user.save()
        assert self.test_user.check_password('password123') is True

    def test_validate_email_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            new_user = User.objects.create(email='robert@gmail.com',
                                           first_name='Name',
                                           last_name='Last Name',
                                           country='Country',
                                           city='City',
                                           address='Address',
                                           mobile_phone='+53 00000000',
                                           password='password123')

    def test_validate_mobile_phone_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            new_user = User.objects.create(email='email@gmail.com',
                                           first_name='Name',
                                           last_name='Last Name',
                                           country='Country',
                                           city='City',
                                           address='Address',
                                           mobile_phone='+53 59876543',
                                           password='password123')

    def test_update_user_with_invalid_email_format(self):
        with self.assertRaises(ValidationError):
            self.test_user.email = 'email'
            self.test_user.full_clean()
            self.test_user.save()

    def test_update_user_with_invalid_mobile_phone_format(self):
        with self.assertRaises(ValidationError):
            self.test_user.mobile_phone = '59002099'
            self.test_user.full_clean()
            self.test_user.save()

    def test_update_user_with_non_numeric_characters_in_mobile_phone_(self):
        with self.assertRaises(ValidationError):
            self.test_user.mobile_phone = '+000 590020aaa&'
            self.test_user.full_clean()
            self.test_user.save()

    def test_update_user_with_numbers_or_simbols_in_names(self):
        with self.assertRaises(ValidationError):
            self.test_user.first_name = 'pedro123'
            self.test_user.last_name = 'Torres  $5541'
            self.test_user.country = 'España'
            self.test_user.city = '990909'
            self.test_user.full_clean()
            self.test_user.save()

    def test_upper_camel_case_names_method(self):
        new_user = User.objects.create(email='migue@gmail.com',
                                       first_name='miguel',
                                       last_name='PEREZ',
                                       country='cuBA',
                                       city='la Habana',
                                       address='Habana Cuba',
                                       mobile_phone='+53 51234567',
                                       password='password123')
        data = {'email': 'migue@gmail.com',
                'first_name': 'Miguel',
                'last_name': 'Perez',
                'country': 'Cuba',
                'city': 'La Habana',
                'address': 'Habana Cuba',
                'mobile_phone': '+53 51234567',
                'is_active': True,
                'is_staff': False,
                'is_superuser': False,
                }
        user = User.objects.filter(email__exact='migue@gmail.com').first()
        self.assertEqual(data, {'email': user.email,
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'country': user.country,
                                'city': user.city,
                                'address': user.address,
                                'mobile_phone': user.mobile_phone,
                                'is_active': user.is_active,
                                'is_staff': user.is_staff,
                                'is_superuser': user.is_superuser,
                                })
