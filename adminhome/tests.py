from django.test import TestCase
from django.urls import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from .views import *
from .forms import CustomUserForm, CustomUserCreationForm, HomeForm
from django.http import HttpRequest
from django.contrib.messages.storage.fallback import FallbackStorage

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
        metedata = {"username":"admin", "password1":"admin", "password2":"admin"}
        
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
        user_metedata = {"username":"new", "password1":"Random@123", "password2":"Random@123"}
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
        user_metedata = {"username":"admin", "password1":"admin", "passwor":"admin"}
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
        self.user = User.objects.create_user(
            username='admin', password='admin')

    def test_signin_view(self):
        response = self.client.get(reverse('adminhome:signin'))
        self.assertEqual(response.status_code, 200)
    
    def test_signin_user_already_signed_in(self):
        request = self.factory.get(reverse('adminhome:signin'))

        request.user = self.user
        
        response = signin(request)

        self.assertEqual(response.status_code, 200)

    def test_signin_success(self):
        user_metedata = {"username":"admin", "password":"admin"}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
    
        request = self.factory.post(reverse('adminhome:signin'), user_metedata)
        setattr(request, 'session', session)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        response = signin(request)
        
        self.assertEqual(response.status_code, 302)
    
    def test_signin_form_invalid(self):
        user_metedata = {"username":"admin", "passwor":"admin"}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
    
        request = self.factory.post(reverse('adminhome:signin'), user_metedata)
        setattr(request, 'session', session)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        response = signin(request)
        
        self.assertEqual(response.status_code, 302)

    def test_signin_fail(self):
        user_metedata = {"username":"admin", "password":"wrongpassword"}
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
    
        request = self.factory.post(reverse('adminhome:signin'), user_metedata)
        setattr(request, 'session', session)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        response = signin(request)
        
        self.assertEqual(response.status_code, 302)

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
        user_metedata = {"username":"username", "password":"password"}
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
