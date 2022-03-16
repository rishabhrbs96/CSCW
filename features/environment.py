from selenium import webdriver
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cameron_rvpark.settings')
django.setup()

from behave import fixture, use_fixture
from django.contrib.auth.models import User
from django.test.runner import DiscoverRunner
from django.test.testcases import LiveServerTestCase


@fixture
def django_test_runner(context):
    django.setup()
    context.test_runner = DiscoverRunner()
    context.test_runner.setup_test_environment()
    context.old_db_config = context.test_runner.setup_databases()
    yield
    context.test_runner.teardown_databases(context.old_db_config)
    context.test_runner.teardown_test_environment()


@fixture
def django_test_case(context):
    context.test_case = LiveServerTestCase
    context.test_case.setUpClass()
    yield
    context.test_case.tearDownClass()
    context.selenium.quit()
    del context.test_case


def before_all(context):
    django.setup()
    context.test_runner = DiscoverRunner()
    context.test_runner.setup_test_environment()
    context.old_db_config = context.test_runner.setup_databases()
    yield
    context.test_runner.teardown_databases(context.old_db_config)
    context.test_runner.teardown_test_environment()


def after_scenario(context, scenario):
    try:
        # Signout
        if context.browser.find_element_by_id("id_sign_out_button"):
            context.browser.find_element_by_id("id_sign_out_button").click()
        else:
            context.browser.find_element_by_xpath("//*[@id='navbarResponsive']/a/button").click()

    except:
        pass


def before_all(context):
    context.browser = webdriver.Chrome()
    context.browser.implicitly_wait(1)
    context.server_home_page_url = "https://test-rv-park.herokuapp.com/"
    context.server_signin_url = context.server_home_page_url + "signin/"
    context.server_admin_dashboard_url = context.server_home_page_url + "edithome/"
    context.server_signup_url = context.server_home_page_url + "signup/"
    context.admin_user_name = os.environ['ADMIN_USERNAME']
    context.admin_password = os.environ['ADMIN_PASSWORD']


def after_all(context):
    context.browser.quit()


def before_feature(context,feature):
    pass

