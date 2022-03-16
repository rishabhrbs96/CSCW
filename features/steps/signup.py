from behave import *
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
import string

use_step_matcher("re")


@given("I am on signup page")
def step_impl(context):
    br = context.browser
    br.get(context.server_signup_url)


@when("I submit a valid username and password in the signup page")
def step_impl(context):
    username = context.browser.find_element_by_id("id_username")
    letters = string.ascii_letters
    new_user_name = ("".join(random.choice(letters) for i in range(7)))
    username.send_keys(new_user_name)

    password = context.browser.find_element_by_id("id_password1")
    password.send_keys(context.admin_password)
    password = context.browser.find_element_by_id("id_password2")
    password.send_keys(context.admin_password)

    # Locate Sign Up button and click on it
    context.browser.find_element_by_id("id_sign_up_button").click()


@then("I am logged in and am redirected to the admin dashboard page")
def step_impl(context):
    url = context.browser.current_url
    context.test.assertEquals(url, context.server_admin_dashboard_url)


@when("I submit a valid username and incorrect passwords in the signup page")
def step_impl(context):
    username = context.browser.find_element_by_id("id_username")
    username.send_keys(context.admin_user_name)

    password = context.browser.find_element_by_id("id_password1")
    password.send_keys("Test@123")
    password = context.browser.find_element_by_id("id_password2")
    password.send_keys("test@123")

    # Locate Sign Up button and click on it
    context.browser.find_element_by_id("id_sign_up_button").click()


@then("I see an error message and I am on the signup page")
def step_impl(context):
    url = context.browser.current_url
    context.test.assertEquals(url, context.server_signup_url)

    # TODO: Check error message.


@when("I submit a valid username and an invalid password in the signup page")
def step_impl(context):
    username = context.browser.find_element_by_id("id_username")
    username.send_keys("test")

    password = context.browser.find_element_by_id("id_password1")
    password.send_keys("five")
    password = context.browser.find_element_by_id("id_password2")
    password.send_keys("five")


@when("I leave both the password fields empty and submit a valid username in the signup page")
def step_impl(context):
    username = context.browser.find_element_by_id("id_username")
    username.send_keys("test")

    password = context.browser.find_element_by_id("id_password1")
    password.send_keys("")
    password = context.browser.find_element_by_id("id_password2")
    password.send_keys("")

    # Locate Sign Up button and click on it
    context.browser.find_element_by_id("id_sign_up_button").click()


@when("I leave the username field empty and submit a valid password in the signup page")
def step_impl(context):
    username = context.browser.find_element_by_id("id_username")
    username.send_keys("")

    password = context.browser.find_element_by_id("id_password1")
    password.send_keys("password!")
    password = context.browser.find_element_by_id("id_password2")
    password.send_keys("password!")

    # Locate Sign Up button and click on it
    context.browser.find_element_by_id("id_sign_up_button").click()


@when("I leave one of the password fields empty and submit a valid username in the signup page")
def step_impl(context):
    username = context.browser.find_element_by_id("id_username")
    username.send_keys("test")

    password = context.browser.find_element_by_id("id_password1")
    password.send_keys("HelloWorld!")
    password = context.browser.find_element_by_id("id_password2")
    password.send_keys("")

    # Locate Sign Up button and click on it
    context.browser.find_element_by_id("id_sign_up_button").click()


@when("I submit existing username in the signup page")
def step_impl(context):
    username = context.browser.find_element_by_id("id_username")
    username.send_keys(context.admin_user_name)

    password = context.browser.find_element_by_id("id_password1")
    password.send_keys(context.admin_password)
    password = context.browser.find_element_by_id("id_password2")
    password.send_keys(context.admin_password)

    # Locate Sign Up button and click on it
    context.browser.find_element_by_id("id_sign_up_button").click()
