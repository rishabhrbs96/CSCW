from behave import *
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

use_step_matcher("re")


@given("I am on login page")
def step_impl(context):
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # context.selenium = webdriver.chrome(options=chrome_options)
    br = context.browser
    br.get(context.server_signin_url)
    context.test.assertEquals(context.browser.current_url, context.server_signin_url)


@when("I submit a valid login credential")
def step_impl(context):
    username = context.browser.find_element_by_id("id_username")
    username.send_keys(context.admin_user_name)

    password = context.browser.find_element_by_id("id_password")
    password.send_keys(context.admin_password)

    # Locate login button and click on it
    context.browser.find_element_by_id("id_sign_in_button").click()


@then("I am redirected to the admin dashboard page")
def step_impl(context):
    url = context.browser.current_url
    context.test.assertEquals(url, context.server_admin_dashboard_url)


@given("I am logged in")
def step_impl(context):
    context.execute_steps(u"""
         Given I am on login page
         When I submit a valid login credential
    """)

    pass


@when("I hit the logout button")
def step_impl(context):
    context.browser.find_element_by_id("id_sign_out_button").click()


@then("I am logged out and am redirected to the home page")
def step_impl(context):
    url = context.browser.current_url
    context.test.assertEquals(url, context.server_home_page_url)


@when("I submit an invalid login credential")
def step_impl(context):
    username = context.browser.find_element_by_id("id_username")
    username.send_keys(context.admin_user_name)

    password = context.browser.find_element_by_id("id_password")
    password.send_keys("invalid_password")

    # Locate login button and click on it
    context.browser.find_element_by_id("id_sign_in_button").click()


@then("I remain on the login page")
def step_impl(context):
    url = context.browser.current_url
    context.test.assertEquals(url, context.server_signin_url)


@when("I leave the username field blank and enter a password")
def step_impl(context):
    username = context.browser.find_element_by_id("id_username")
    username.send_keys("")

    password = context.browser.find_element_by_id("id_password")
    password.send_keys("test123")

    # Locate login button and click on it
    context.browser.find_element_by_id("id_sign_in_button").click()


@when("I leave the password field blank and enter an username")
def step_impl(context):
    username = context.browser.find_element_by_id("id_username")
    username.send_keys(context.admin_user_name)

    password = context.browser.find_element_by_id("id_password")
    password.send_keys("")

    # Locate login button and click on it
    context.browser.find_element_by_id("id_sign_in_button").click()

    
