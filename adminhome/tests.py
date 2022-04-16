from django.test import TestCase, Client
from django.urls import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from .views import *
from .forms import CustomUserForm, CustomUserCreationForm, HomeForm, ParkingSpotForm, ParkingCategoryForm
from .models import ParkingSpot, ParkingCategory
from django.http import HttpRequest
from django.contrib.messages.storage.fallback import FallbackStorage
from http import HTTPStatus
import os
import boto3, botocore
from moto import mock_s3


@mock_s3
class TestDoEdit(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', password='pass')
        self.super_user = User.objects.create_superuser(
            username='useradmin', password='passadmin')

    def test_success_not_staff(self):
        self.client.login(username='user', password='pass')
        metedata = {"username": "admin", "password1": "admin", "password2": "admin"}

        request = self.factory.post(reverse('adminhome:doedit'), metedata)
        request.user = self.user

        response = doedit(request)
        self.assertEqual(response.status_code, 302)

    @mock_s3
    def test_success_is_staff(self):
        metedata = {
            "carousel_image_0": "c1i",
            "carousel_header_0": "Slide 1 Header",
            "carousel_body_0": "Slide 1 Body",
            "carousel_image_1": "c2i",
            "carousel_header_1": "Slide 2 Header",
            "carousel_body_1": "Slide 2 Body",
            "carousel_image_2": "c3i",
            "carousel_header_2": "Slide 3 Header",
            "carousel_body_2": "Slide 3 Body",
            "about_header": "About Us",
            "about_body": "Quickly design and customize responsive mobile-first sites with Bootstrap, the world’s most popular front-end open source toolkit, featuring Sass variables and mixins, responsive grid system, extensive prebuilt components, and powerful JavaScript plugins.",
            "ameneties_header": "Ameneties We Offer",
            "ameneties_body": "Quickly design and customize responsive mobile-first sites with Bootstrap, the world’s most popular front-end open source toolkit, featuring Sass variables and mixins, responsive grid system, extensive prebuilt components, and powerful JavaScript plugins.",
            "phone": "+1 (987) 654 3210",
            "email": "techcameronrvpark@gmail.com",
            "location": "College Station, TX",
        }

        self.client.login(username='useradmin', password='passadmin')
        MY_BUCKET = 'cameron-rv-park'
        client = boto3.client(
            "s3",
            region_name="us-east-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
        )
        try:
            s3 = boto3.resource(
                "s3",
                region_name="us-east-1",
                aws_access_key_id="fake_access_key",
                aws_secret_access_key="fake_secret_key",
            )
            s3.meta.client.head_bucket(Bucket=MY_BUCKET)
        except botocore.exceptions.ClientError:
            pass
        else:
            err = "{bucket} should not exist.".format(bucket=MY_BUCKET)
            raise EnvironmentError(err)
        client.create_bucket(Bucket=MY_BUCKET)

        request = self.factory.post(reverse('adminhome:doedit'), metedata)
        request.user = self.super_user

        response = doedit(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(True, True)

        s3 = boto3.resource(
            "s3",
            region_name="us-east-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
        )
        bucket = s3.Bucket(MY_BUCKET)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()


class TestEditHome(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', password='pass')
        self.super_user = User.objects.create_superuser(username='useradmin', password='passadmin')

    def test_user_not_authenticated(self):
        request = self.factory.get(reverse('adminhome:edithome'))
        # AnonymousUser are not authenticated
        request.user = AnonymousUser()
        response = edithome(request)
        self.assertEqual(response.status_code, 302)

    def test_user_is_authenticated(self):
        # user is not authenticated
        self.client.login(username='user', password='pass')
        request = self.factory.get(reverse('adminhome:edithome'))
        request.user = self.user
        response = edithome(request)
        self.assertEqual(response.status_code, 302)

    def test_user_is_authenticated_super_user(self):
        # user is not authenticated
        self.client.login(username='user', password='pass')
        request = self.factory.get(reverse('adminhome:edithome'))
        request.user = self.super_user
        response = edithome(request)
        self.assertEqual(response.status_code, 200)


class TestSignupView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='admin', password='admin')

    def test_signup_view(self):
        response = self.client.get(reverse('adminhome:signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_success_already_logged_in(self):
        request = self.factory.get(reverse('adminhome:signup'))
        request.user = self.user
        response = signup(request)
        self.assertEqual(response.status_code, 200)

    def test_signinup_success_not_logged_in(self):
        user_metedata = {"username": "new", "password1": "Random@123", "password2": "Random@123"}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()

        request = self.factory.post(reverse('adminhome:signup'), user_metedata)
        setattr(request, 'method', 'POST')
        setattr(request, 'session', session)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = signup(request)

        self.assertEqual(response.status_code, 302)

    def test_signinup_form_invalid(self):
        user_metedata = {"username": "admin", "password1": "admin", "passwor": "admin"}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()

        request = self.factory.post(reverse('adminhome:signup'), user_metedata)
        setattr(request, 'session', session)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = signup(request)

        self.assertEqual(response.status_code, 200)


class TestSigninView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='admin', password='admin')
        self.admin = User.objects.create_superuser(username='superuser', password='superuser')

    def test_signin_view(self):
        response = self.client.get(reverse('adminhome:signin'))
        self.assertEqual(response.status_code, 200)

    def test_signin_user_already_signed_in(self):
        request = self.factory.get(reverse('adminhome:signin'))

        request.user = self.user

        response = signin(request)

        self.assertEqual(response.status_code, 200)

    def test_signin_success(self):
        user_metedata = {"username": "admin", "password": "admin"}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()

        request = self.factory.post(reverse('adminhome:signin'), user_metedata)
        request.user = self.user

        setattr(request, 'session', session)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = signin(request)
        response.client = Client()

        self.assertRedirects(response, '/', 302)

    def test_signin_success_for_admin_or_staff(self):
        login_metadata = {"username": "superuser", "password": "superuser"}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()

        request = self.factory.post(reverse('adminhome:signin'), login_metadata)
        request.user = self.admin

        setattr(request, 'session', session)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = signin(request)
        response.client = Client()

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, '/adminhome/')

    def test_signin_form_invalid(self):
        user_metedata = {"username": "admin", "passwor": "admin"}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()

        request = self.factory.post(reverse('adminhome:signin'), user_metedata)
        setattr(request, 'session', session)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = signin(request)

        self.assertEqual(response.status_code, 200)

    def test_signin_fail(self):
        user_metedata = {"username": "admin", "password": "wrongpassword"}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()

        request = self.factory.post(reverse('adminhome:signin'), user_metedata)
        setattr(request, 'session', session)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = signin(request)

        self.assertEqual(response.status_code, 200)


class TestIndexView(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('adminhome:index'))
        self.assertEqual(response.status_code, 200)


class TestCustomUserCreationForm(TestCase):
    def test_user_creation_form_correct(self):
        user_form = CustomUserCreationForm(None)

        self.assertEqual(len(user_form.visible_fields()), 3)

    def test_user_creation_form_incorrect(self):
        try:
            user_form = CustomUserCreationForm(None, data={})
            self.fail("fail")
        except Exception as e:
            self.assertEqual(type(e), TypeError)


class TestCustomUserForm(TestCase):
    def test_user_form_correct(self):
        user_metedata = {"username": "username", "password": "password"}
        user_form = CustomUserForm(None, data=user_metedata)

        self.assertEqual(len(user_form.visible_fields()), 2)

    def test_user_form_incorrect(self):
        try:
            user_form = CustomUserForm(None, data={})
            self.fail("fail")
        except Exception as e:
            self.assertEqual(type(e), AssertionError)


class TestHomeForm(TestCase):
    def test_home_form_correct(self):
        home_metedata = {
            "carousel": [
                {
                    "image": "c1i",
                    "header": "Slide 1 Header",
                    "body": "Slide 1 Body"
                },
                {
                    "image": "c2i",
                    "header": "Slide 2 Header",
                    "body": "Slide 2 Body"
                },
                {
                    "image": "c3i",
                    "header": "Slide 3 Header",
                    "body": "Slide 3 Body"
                }
            ],
            "about": {
                "about_header": "About Us",
                "about_body": "Quickly design and customize responsive mobile-first sites with Bootstrap, the world’s most popular front-end open source toolkit, featuring Sass variables and mixins, responsive grid system, extensive prebuilt components, and powerful JavaScript plugins."
            },
            "ameneties": {
                "ameneties_header": "Ameneties We Offer",
                "ameneties_body": "Quickly design and customize responsive mobile-first sites with Bootstrap, the world’s most popular front-end open source toolkit, featuring Sass variables and mixins, responsive grid system, extensive prebuilt components, and powerful JavaScript plugins."
            },
            "contact": {
                "phone": "phone",
                "email": "sethji@billionaire.com",
                "location": "location"
            }
        }
        home_form = HomeForm(None, extra=home_metedata)

        self.assertEqual(len(home_form.visible_fields()), 16)

    def test_home_form_incorrect(self):
        try:
            home_form = HomeForm(None, extra={})
            self.fail("fail")
        except Exception as e:
            self.assertEqual(type(e), KeyError)


class TestParkingCategoryForm(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', password='pass')
        self.super_user = User.objects.create_superuser(username='useradmin', password='passadmin')
        self.parking_category = ParkingCategory.objects.create(name="pc_1", size=1.00, daily_rate=1.0,
                                                               weekly_rate=1.0,
                                                               monthly_rate=1.0,
                                                               utility_conversion_rate=1.0,
                                                               is_active=True,
                                                               cancellation_penalty=1.0,
                                                               cancellation_time_window=1)
        self.parking_spot = ParkingSpot.objects.create(name="test_spot", parking_category_id=self.parking_category,
                                                       is_active=True)

    def test_create_parking_category_form_valid(self):
        form = ParkingCategoryForm({'name': "test",
                                    'size': '1',
                                    'daily_rate': '1',
                                    'weekly_rate': '1',
                                    'monthly_rate': '1',
                                    'utility_conversion_rate': '1',
                                    'is_active': True,
                                    'cancellation_penalty': '1',
                                    'cancellation_time_window': '1'})

        self.assertTrue(form.is_valid())

    def test_create_parking_category_form_invalid(self):
        form = ParkingCategoryForm({'name': "test",
                                    'size': '1',
                                    'daily_rate': '1',
                                    'weekly_rate': '1',
                                    'monthly_rate': '1',
                                    'utility_conversion_rate': '1',
                                    'is_active': True,
                                    'cancellation_penalty': '',
                                    'cancellation_time_window': '1'})
        self.assertFalse(form.is_valid())


class TestParkingCategoryView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create_user(
            username='user', password='pass')
        self.super_user = User.objects.create_superuser(username='useradmin', password='passadmin')
        self.parking_category = ParkingCategory.objects.create(name="pc_1", size=1.00, daily_rate=1.0,
                                                               weekly_rate=1.0,
                                                               monthly_rate=1.0,
                                                               utility_conversion_rate=1.0,
                                                               is_active=True,
                                                               cancellation_penalty=1.0,
                                                               cancellation_time_window=1)

    def test_create_parking_category_not_admin(self):
        # not an admin user
        self.client.login(username='user', password='pass')
        request = self.factory.get(reverse('adminhome:createparkingcategory'))
        request.user = self.user
        response = createparkingcategory(request)
        self.assertEqual(response.status_code, 302)

    def test_view_parking_category_not_admin(self):
        # not an admin user
        self.client.login(username='user', password='pass')

        request = self.factory.get(reverse('adminhome:viewparkingcategory'))
        request.user = self.user
        response = viewparkingcategory(request)
        self.assertEqual(response.status_code, 302)

    def test_view_one_parking_category_not_admin(self):
        # not an admin user
        self.client.login(username='user', password='pass')

        request = self.factory.get(reverse('adminhome:viewoneparkingcategory', kwargs={'pk': 1}))
        request.user = self.user
        response = viewoneparkingcategory(request, 1)
        self.assertEqual(response.status_code, 302)

    def test_update_parking_category_not_admin(self):
        # not an admin user
        self.client.login(username='user', password='pass')
        request = self.factory.get(reverse('adminhome:updateparkingcategory', kwargs={'pk': 1}))
        request.user = self.user
        response = updateparkingcategory(request, 1)
        self.assertEqual(response.status_code, 302)

    def test_delete_parking_category_not_admin(self):
        # not an admin user
        self.client.login(username='user', password='pass')
        request = self.factory.get(reverse('adminhome:deleteparkingcategory', kwargs={'pk': 1}))
        request.user = self.user
        response = deleteparkingcategory(request, 1)
        self.assertEqual(response.status_code, 302)

    def test_view_parking_category_admin(self):
        self.client.login(username='useradmin', password='passadmin')
        request = self.factory.get(reverse('adminhome:viewparkingcategory'))
        request.user = self.super_user
        response = viewparkingcategory(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_one_parking_category_admin(self):
        self.client.login(username='useradmin', password='passadmin')
        request = self.factory.get(reverse('adminhome:viewoneparkingcategory', kwargs={'pk': 1}))
        request.user = self.super_user
        response = viewoneparkingcategory(request, 1)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_delete_parking_category_admin_render(self):
        # not an admin user
        self.client.login(username='useradmin', password='passadmin')
        request = self.factory.get(reverse('adminhome:deleteparkingcategory', kwargs={'pk': 1}))
        request.user = self.super_user
        response = deleteparkingcategory(request, 1)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_delete_parking_category_admin(self):
        metedata = {}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        self.client.login(username='useradmin', password='passadmin')
        request = self.factory.post(reverse('adminhome:deleteparkingcategory', kwargs={'pk': 1}))
        setattr(request, 'method', 'POST')
        setattr(request, 'session', session)

        request.user = self.super_user
        response = deleteparkingcategory(request, 1)

        self.assertEqual(response.status_code, 302)

    def test_create_parking_category_admin_render(self):
        self.client.login(username='useradmin', password='passadmin')
        request = self.factory.get(reverse('adminhome:createparkingcategory'))
        request.user = self.super_user
        response = createparkingcategory(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_parking_category_valid(self):
        ParkingCategory.objects.all().delete()
        count = ParkingCategory.objects.count()
        parking_category_data = {'name': "test",
                                 'size': '1.00',
                                 'daily_rate': '1.00',
                                 'weekly_rate': '1.00',
                                 'monthly_rate': '1.00',
                                 'utility_conversion_rate': '1.00',
                                 'is_active': True,
                                 'cancellation_penalty': '1.00',
                                 'cancellation_time_window': '1.00'}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        self.client.login(username='useradmin', password='passadmin')
        request = self.client.post(reverse('adminhome:createparkingcategory'), parking_category_data)
        setattr(request, 'method', 'POST')
        setattr(request, 'session', session)
        request.user = self.super_user

        self.assertEqual(ParkingCategory.objects.count(), count + 1)
        self.assertEqual(request.url, "/parkingcategory/2/")
        ParkingCategory.objects.all().delete()

    def test_create_parking_category_invalid(self):
        count = ParkingCategory.objects.count()

        parking_category_data = {'name': "test",
                                 'size': '1',
                                 'daily_rate': '1',
                                 'weekly_rate': '1',
                                 'monthly_rate': '1',
                                 'utility_conversion_rate': '1',
                                 'is_active': True,
                                 'cancellation_penalty': '',
                                 'cancellation_time_window': '1'}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        self.client.login(username='useradmin', password='passadmin')
        request = self.client.post(reverse('adminhome:createparkingcategory'), parking_category_data)
        request.user = self.super_user

        self.assertEqual(ParkingCategory.objects.count(), count)

    def test_update_parking_category_valid(self):
        ParkingCategory.objects.all().delete()
        parking_category_data = {'name': "test",
                                 'size': '1.00',
                                 'daily_rate': '1.00',
                                 'weekly_rate': '1.00',
                                 'monthly_rate': '1.00',
                                 'utility_conversion_rate': '1.00',
                                 'is_active': True,
                                 'cancellation_penalty': '1.00',
                                 'cancellation_time_window': '1.00'}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        self.client.login(username='useradmin', password='passadmin')
        request = self.client.post(reverse('adminhome:createparkingcategory'), parking_category_data)
        setattr(request, 'method', 'POST')
        setattr(request, 'session', session)
        request.user = self.super_user

        parking_category_data = {'name': "test2",
                                 'size': '2.00',
                                 'daily_rate': '1.00',
                                 'weekly_rate': '1.00',
                                 'monthly_rate': '1.00',
                                 'utility_conversion_rate': '1.00',
                                 'is_active': True,
                                 'cancellation_penalty': '1.00',
                                 'cancellation_time_window': '1.00'}

        request = self.factory.post(reverse('adminhome:updateparkingcategory', kwargs={'pk': 2}), parking_category_data)
        setattr(request, 'method', 'POST')
        setattr(request, 'session', session)
        request.user = self.super_user
        response = updateparkingcategory(request, 2)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/parkingcategory/2/")
        ParkingCategory.objects.all().delete()

    def test_update_parking_category_invalid(self):
        ParkingCategory.objects.all().delete()
        parking_category_data = {'name': "test",
                                 'size': '1.00',
                                 'daily_rate': '1.00',
                                 'weekly_rate': '1.00',
                                 'monthly_rate': '1.00',
                                 'utility_conversion_rate': '1.00',
                                 'is_active': True,
                                 'cancellation_penalty': '1.00',
                                 'cancellation_time_window': '1.00'}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        self.client.login(username='useradmin', password='passadmin')
        request = self.client.post(reverse('adminhome:createparkingcategory'), parking_category_data)
        setattr(request, 'method', 'POST')
        setattr(request, 'session', session)
        request.user = self.super_user

        parking_category_data = {'name': "test2",
                                 'size': '2.00',
                                 'daily_rate': '1.00',
                                 'weekly_rate': '1.00',
                                 'monthly_rate': '1.00',
                                 'utility_conversion_rate': '1.00',
                                 'is_active': True,
                                 'cancellation_penalty': '',
                                 'cancellation_time_window': '1.00'}

        request = self.factory.post(reverse('adminhome:updateparkingcategory', kwargs={'pk': 2}), parking_category_data)
        setattr(request, 'method', 'POST')
        setattr(request, 'session', session)
        request.user = self.super_user
        response = updateparkingcategory(request, 2)

        self.assertEqual(response.status_code, 200)
        ParkingCategory.objects.all().delete()


class TestParkingSpotView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create_user(
            username='user', password='pass')
        self.super_user = User.objects.create_superuser(username='useradmin', password='passadmin')
        self.parking_category = ParkingCategory.objects.create(name="pc_1", size=1.00, daily_rate=1.0,
                                                               weekly_rate=1.0,
                                                               monthly_rate=1.0,
                                                               utility_conversion_rate=1.0,
                                                               is_active=True,
                                                               cancellation_penalty=1.0,
                                                               cancellation_time_window=1)
        self.parking_spot = ParkingSpot.objects.create(name="test_spot", parking_category_id=self.parking_category,
                                                       is_active=True)

    def test_create_parking_spot_not_admin(self):
        # not an admin user
        self.client.login(username='user', password='pass')
        request = self.factory.get(reverse('adminhome:createparkingspot'))
        request.user = self.user
        response = createparkingspot(request)
        self.assertEqual(response.status_code, 302)

    def test_view_parking_spot_not_admin(self):
        # not an admin user
        self.client.login(username='user', password='pass')

        request = self.factory.get(reverse('adminhome:viewparkingspot'))
        request.user = self.user
        response = viewparkingspot(request)
        self.assertEqual(response.status_code, 302)

    def test_view_one_parking_spot_not_admin(self):
        # not an admin user
        self.client.login(username='user', password='pass')

        request = self.factory.get(reverse('adminhome:viewoneparkingspot', kwargs={'pk': 1}))
        request.user = self.user
        response = viewoneparkingspot(request, 1)
        self.assertEqual(response.status_code, 302)

    def test_update_parking_spot_not_admin(self):
        # not an admin user
        self.client.login(username='user', password='pass')
        request = self.factory.get(reverse('adminhome:updateparkingspot', kwargs={'pk': 1}))
        request.user = self.user
        response = updateparkingspot(request, 1)
        self.assertEqual(response.status_code, 302)

    def test_delete_parking_spot_not_admin(self):
        # not an admin user
        self.client.login(username='user', password='pass')
        request = self.factory.get(reverse('adminhome:deleteparkingspot', kwargs={'pk': 1}))
        request.user = self.user
        response = deleteparkingspot(request, 1)
        self.assertEqual(response.status_code, 302)

    def test_view_parking_spot_admin(self):
        self.client.login(username='useradmin', password='passadmin')
        request = self.factory.get(reverse('adminhome:viewparkingspot'))
        request.user = self.super_user
        response = viewparkingspot(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_one_parking_spot_admin(self):
        self.client.login(username='useradmin', password='passadmin')
        request = self.factory.get(reverse('adminhome:viewoneparkingspot', kwargs={'pk': 1}))
        request.user = self.super_user
        response = viewoneparkingspot(request, 1)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_delete_parking_spot_admin_render(self):
        # not an admin user
        self.client.login(username='useradmin', password='passadmin')
        request = self.factory.get(reverse('adminhome:deleteparkingspot', kwargs={'pk': 1}))
        request.user = self.super_user
        response = deleteparkingspot(request, 1)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_delete_parking_spot_admin(self):
        metedata = {}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        self.client.login(username='useradmin', password='passadmin')
        request = self.factory.post(reverse('adminhome:deleteparkingspot', kwargs={'pk': 1}))
        setattr(request, 'method', 'POST')
        setattr(request, 'session', session)

        request.user = self.super_user
        response = deleteparkingspot(request, 1)

        self.assertEqual(response.status_code, 302)

    def test_create_parking_spot_admin_render(self):
        self.client.login(username='useradmin', password='passadmin')
        request = self.factory.get(reverse('adminhome:createparkingspot'))
        request.user = self.super_user
        response = createparkingspot(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_parking_spot_valid(self):
        ParkingSpot.objects.all().delete()
        count = ParkingSpot.objects.count()
        parking_spot_data = {'name': "test_spot_2",
                             'parking_category_id': '1',
                             'is_active': True}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        self.client.login(username='useradmin', password='passadmin')
        request = self.client.post(reverse('adminhome:createparkingspot'), parking_spot_data)
        setattr(request, 'method', 'POST')
        setattr(request, 'session', session)
        request.user = self.super_user

        self.assertEqual(ParkingSpot.objects.count(), count + 1)
        ParkingSpot.objects.all().delete()

    def test_create_parking_spot_invalid(self):
        count = ParkingSpot.objects.count()

        parking_spot_data = {'name': "test_spot_2",
                             'parking_category_id': '',
                             'is_active': True}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        self.client.login(username='useradmin', password='passadmin')
        request = self.client.post(reverse('adminhome:createparkingspot'), parking_spot_data)
        request.user = self.super_user

        self.assertEqual(ParkingSpot.objects.count(), count)

    def test_update_parking_spot_valid(self):
        ParkingSpot.objects.all().delete()
        parking_spot_data = {'name': "test_spot_2",
                             'parking_category_id': '1',
                             'is_active': True}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        self.client.login(username='useradmin', password='passadmin')
        request = self.client.post(reverse('adminhome:createparkingspot'), parking_spot_data)
        setattr(request, 'method', 'POST')
        setattr(request, 'session', session)
        request.user = self.super_user

        parking_spot_data = {'name': "test_spot_3",
                             'parking_category_id': '1',
                             'is_active': True}

        request = self.factory.post(reverse('adminhome:updateparkingspot', kwargs={'pk': 2}), parking_spot_data)
        setattr(request, 'method', 'POST')
        setattr(request, 'session', session)
        request.user = self.super_user
        response = updateparkingspot(request, 2)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/parkingspot/2/")
        ParkingSpot.objects.all().delete()

    def test_update_parking_spot_invalid(self):
        ParkingSpot.objects.all().delete()
        parking_spot_data = {'name': "test_spot_2",
                             'parking_category_id': '1',
                             'is_active': True}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        self.client.login(username='useradmin', password='passadmin')
        request = self.client.post(reverse('adminhome:createparkingspot'), parking_spot_data)
        setattr(request, 'method', 'POST')
        setattr(request, 'session', session)
        request.user = self.super_user

        parking_spot_data = {'name': "test_spot_2",
                             'parking_category_id': '',
                             'is_active': True}

        request = self.factory.post(reverse('adminhome:updateparkingspot', kwargs={'pk': 2}), parking_spot_data)
        setattr(request, 'method', 'POST')
        setattr(request, 'session', session)
        request.user = self.super_user
        response = updateparkingspot(request, 2)

        self.assertEqual(response.status_code, 200)
        ParkingSpot.objects.all().delete()


# model Tests
class TesetParkingSpotModel(TestCase):

    def test_parking_spot_model(self):
        parking_category = ParkingCategory.objects.create(name="pc_1", size=1, daily_rate=1,
                                                          weekly_rate=1,
                                                          monthly_rate=1,
                                                          utility_conversion_rate=1,
                                                          is_active=True,
                                                          cancellation_penalty=1,
                                                          cancellation_time_window=1)

        parking_spot = ParkingSpot.objects.create(name="test_spot", parking_category_id=parking_category,
                                                  is_active=True)

        self.assertTrue(isinstance(parking_spot, ParkingSpot))
        self.assertEqual(str(parking_spot), parking_spot.name)


class TesetParkingCategoryModel(TestCase):

    def test_parking_category_model(self):
        parking_category = ParkingCategory.objects.create(name="pc_1", size=1, daily_rate=1,
                                                          weekly_rate=1,
                                                          monthly_rate=1,
                                                          utility_conversion_rate=1,
                                                          is_active=True,
                                                          cancellation_penalty=1,
                                                          cancellation_time_window=1)

        self.assertTrue(isinstance(parking_category, ParkingCategory))
        self.assertEqual(str(parking_category), parking_category.name)
