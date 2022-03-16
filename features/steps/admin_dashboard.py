from behave import *

use_step_matcher("re")


@when("I select the Edit Home Page Contents option on admin dashboard")
def step_impl(context):
    context.browser.find_element_by_link_text("Edit Home Page Contents").click()


@then("I am redirected to the Edit Home Page Contents page")
def step_impl(context):
    context.test.assertEquals(context.browser.current_url[:-1], context.server_admin_dashboard_url)


@given("I am on the Edit Home Page Contents Page")
def step_impl(context):
    context.execute_steps(u"""
             Given I am on login page
             When I submit a valid login credential
             And I select the Edit Home Page Contents option on admin dashboard
        """)


use_step_matcher("parse")
@when("I modify the About Us Header field to {text}")
def step_impl(context,text):
    about_us_field = context.browser.find_element_by_id("id_about_header")
    about_us_field.clear()
    about_us_field.send_keys(text)


@when("hit the submit button")
def step_impl(context):
    context.browser.find_element_by_xpath('//button[text()="Submit"]').submit()


use_step_matcher("parse")
@then("the text for About Us Header field should match {text}")
def step_impl(context, text):
    about_us_field = context.browser.find_element_by_id("id_about_header")
    context.test.assertEquals(about_us_field.get_attribute('value'), text)
    context.browser.get(context.server_home_page_url)
    about_us_home = context.browser.find_element_by_xpath("/html/body/div[1]/div/h1")
    context.test.assertEquals(about_us_home.get_attribute('textContent'), text)
    context.browser.get(context.server_admin_dashboard_url)
    # context.browser.find_element_by_xpath("//*[@id='navbarResponsive']/a/button").click()

use_step_matcher("parse")
@when("I modify the About Us Body field to {text}")
def step_impl(context,text):
    about_us_field = context.browser.find_element_by_id("id_about_body")
    about_us_field.clear()
    about_us_field.send_keys(text)

use_step_matcher("parse")
@then("the text for About Us Body field should match {text}")
def step_impl(context, text):
    about_us_field = context.browser.find_element_by_id("id_about_body")
    context.test.assertEquals(about_us_field.get_attribute('value'), text)
    context.browser.get(context.server_home_page_url)
    about_us_home = context.browser.find_element_by_xpath("//*[@id='about']/div/div/p")
    context.test.assertEquals(about_us_home.get_attribute('textContent'), text)
    context.browser.get(context.server_admin_dashboard_url)
    # need to handle logout scenario from the home page


use_step_matcher("parse")
@when("I modify the Amenities Header field to {text}")
def step_impl(context, text):
    ameneties_header_field = context.browser.find_element_by_id("id_ameneties_header")
    ameneties_header_field.clear()
    ameneties_header_field.send_keys(text)

use_step_matcher("parse")
@then("the text for Amenities Header field should match {text}")
def step_impl(context, text):
    ameneties_header_field = context.browser.find_element_by_id("id_ameneties_header")
    context.test.assertEquals(ameneties_header_field.get_attribute('value'), text)
    context.browser.get(context.server_home_page_url)
    ameneties_home = context.browser.find_element_by_xpath("//*[@id='ameneties']/h1")
    context.test.assertEquals(ameneties_home.get_attribute('textContent'), text)
    context.browser.get(context.server_admin_dashboard_url)

use_step_matcher("parse")
@when("I modify the Amenities Body field to {text}")
def step_impl(context,text):
    ameneties_body_field = context.browser.find_element_by_id("id_ameneties_body")
    ameneties_body_field.clear()
    ameneties_body_field.send_keys(text)


use_step_matcher("parse")
@then("the text for Amenities Body field should match {text}")
def step_impl(context, text):
    ameneties_body_field = context.browser.find_element_by_id("id_ameneties_body")
    context.test.assertEquals(ameneties_body_field.get_attribute('value'), text)
    context.browser.get(context.server_home_page_url)
    ameneties_home = context.browser.find_element_by_xpath("//*[@id='ameneties']/div/p")
    context.test.assertEquals(ameneties_home.get_attribute('textContent'), text)
    context.browser.get(context.server_admin_dashboard_url)

use_step_matcher("parse")
@when("I modify the Phone Number field to {text}")
def step_impl(context, text):
    phone_num = context.browser.find_element_by_id("id_phone")
    phone_num.clear()
    phone_num.send_keys(text)

use_step_matcher("parse")
@then("the text for Phone Number field should match {text}")
def step_impl(context, text):
    phone_num = context.browser.find_element_by_id("id_phone")
    context.test.assertEquals(phone_num.get_attribute('value'), text)
    context.browser.get(context.server_home_page_url)
    phone_home = context.browser.find_element_by_xpath("// *[ @ id = 'contactus'] / div / div[2] / ul / li[2] / p")
    context.test.assertEquals(phone_home.get_attribute('textContent'), text)
    context.browser.get(context.server_admin_dashboard_url)



use_step_matcher("parse")
@when("I modify the Email address field to {text}")
def step_impl(context, text):
    email = context.browser.find_element_by_id("id_email")
    email.clear()
    email.send_keys(text)


use_step_matcher("parse")
@then("the text for Email address field should match {text}")
def step_impl(context, text):
    email = context.browser.find_element_by_id("id_email")
    context.test.assertEquals(email.get_attribute('value'), text)
    context.browser.get(context.server_home_page_url)
    email_home = context.browser.find_element_by_xpath("// *[ @ id = 'contactus'] / div / div[2] / ul / li[3] / p")
    context.test.assertEquals(email_home.get_attribute('textContent'), text)
    context.browser.get(context.server_admin_dashboard_url)


use_step_matcher("parse")
@when("I modify the Location field to {text}")
def step_impl(context, text):
    location = context.browser.find_element_by_id("id_location")
    location.clear()
    location.send_keys(text)

use_step_matcher("parse")
@then("the text for Location field should match {text}")
def step_impl(context, text):
    location = context.browser.find_element_by_id("id_location")
    context.test.assertEquals(location.get_attribute('value'), text)
    context.browser.get(context.server_home_page_url)
    location_home = context.browser.find_element_by_xpath("//*[@id='contactus']/div/div[2]/ul/li[1]/p")
    context.test.assertEquals(location_home.get_attribute('textContent'), text)
    context.browser.get(context.server_admin_dashboard_url)


use_step_matcher("parse")
@when("I modify the Carousel 1 Header field to {text}")
def step_impl(context, text):
    carousel_1_header = context.browser.find_element_by_id("id_carousel_header_0")
    carousel_1_header.clear()
    carousel_1_header.send_keys(text)


use_step_matcher("parse")
@then("the text for Carousel 1 Header field should match {text}")
def step_impl(context, text):
    carousel_1_header = context.browser.find_element_by_id("id_carousel_header_0")
    context.test.assertEquals(carousel_1_header.get_attribute('value'), text)
    context.browser.get(context.server_home_page_url)
    carousel_1_header_home = context.browser.find_element_by_xpath("//*[@id='carouselExampleCaptions']/div[2]/div[1]/div/h4")
    context.test.assertEquals(carousel_1_header_home.get_attribute('textContent'), text)
    context.browser.get(context.server_admin_dashboard_url)


use_step_matcher("parse")
@when("I modify the Carousel 1 Contents field to {text}")
def step_impl(context, text):
    carousel_1_body = context.browser.find_element_by_id("id_carousel_body_0")
    carousel_1_body.clear()
    carousel_1_body.send_keys(text)


use_step_matcher("parse")
@then("the text for Carousel 1 Contents field should match {text}")
def step_impl(context, text):
    carousel_1_body = context.browser.find_element_by_id("id_carousel_body_0")
    context.test.assertEquals(carousel_1_body.get_attribute('value'), text)
    context.browser.get(context.server_home_page_url)
    carousel_1_body_home = context.browser.find_element_by_xpath("//*[@id='carouselExampleCaptions']/div[2]/div[1]/div/p")
    context.test.assertEquals(carousel_1_body_home.get_attribute('textContent'), text)
    context.browser.get(context.server_admin_dashboard_url)


use_step_matcher("parse")
@when("I modify the Carousel 2 Header field to {text}")
def step_impl(context, text):
    carousel_2_header = context.browser.find_element_by_id("id_carousel_header_1")
    carousel_2_header.clear()
    carousel_2_header.send_keys(text)


use_step_matcher("parse")
@then("the text for Carousel 2 Header field should match {text}")
def step_impl(context, text):
    carousel_2_header = context.browser.find_element_by_id("id_carousel_header_1")
    context.test.assertEquals(carousel_2_header.get_attribute('value'), text)
    context.browser.get(context.server_home_page_url)
    carousel_2_header_home = context.browser.find_element_by_xpath("//*[@id='carouselExampleCaptions']/div[2]/div[2]/div/h4")
    context.test.assertEquals(carousel_2_header_home.get_attribute('textContent'), text)
    context.browser.get(context.server_admin_dashboard_url)


use_step_matcher("parse")
@when("I modify the Carousel 2 Contents field to {text}")
def step_impl(context, text):
    carousel_2_body = context.browser.find_element_by_id("id_carousel_body_1")
    carousel_2_body.clear()
    carousel_2_body.send_keys(text)


use_step_matcher("parse")
@then("the text for Carousel 2 Contents field should match {text}")
def step_impl(context, text):
    carousel_2_body = context.browser.find_element_by_id("id_carousel_body_1")
    context.test.assertEquals(carousel_2_body.get_attribute('value'), text)
    context.browser.get(context.server_home_page_url)
    carousel_2_body_home = context.browser.find_element_by_xpath("//*[@id='carouselExampleCaptions']/div[2]/div[2]/div/p")
    context.test.assertEquals(carousel_2_body_home.get_attribute('textContent'), text)
    context.browser.get(context.server_admin_dashboard_url)


use_step_matcher("parse")
@when("I modify the Carousel 3 Header field to {text}")
def step_impl(context, text):
    carousel_3_header = context.browser.find_element_by_id("id_carousel_header_2")
    carousel_3_header.clear()
    carousel_3_header.send_keys(text)


use_step_matcher("parse")
@then("the text for Carousel 3 Header field should match {text}")
def step_impl(context, text):
    carousel_3_header = context.browser.find_element_by_id("id_carousel_header_2")
    context.test.assertEquals(carousel_3_header.get_attribute('value'), text)
    context.browser.get(context.server_home_page_url)
    carousel_3_header_home = context.browser.find_element_by_xpath("//*[@id='carouselExampleCaptions']/div[2]/div[3]/div/h4")
    context.test.assertEquals(carousel_3_header_home.get_attribute('textContent'), text)
    context.browser.get(context.server_admin_dashboard_url)


use_step_matcher("parse")
@when("I modify the Carousel 3 Contents field to {text}")
def step_impl(context, text):
    carousel_3_body = context.browser.find_element_by_id("id_carousel_body_2")
    carousel_3_body.clear()
    carousel_3_body.send_keys(text)


use_step_matcher("parse")
@then("the text for Carousel 3 Contents field should match {text}")
def step_impl(context, text):
    carousel_3_body = context.browser.find_element_by_id("id_carousel_body_2")
    context.test.assertEquals(carousel_3_body.get_attribute('value'), text)
    context.browser.get(context.server_home_page_url)
    carousel_3_body_home = context.browser.find_element_by_xpath("//*[@id='carouselExampleCaptions']/div[2]/div[3]/div/p")
    context.test.assertEquals(carousel_3_body_home.get_attribute('textContent'), text)
    context.browser.get(context.server_admin_dashboard_url)
