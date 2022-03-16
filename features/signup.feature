Feature: Signup Page

# Scenario: User enters all the fields correctly on the signup page and is able to create an account.
#    Given I am on signup page
#    When I submit a valid username and password in the signup page
#    Then I am logged in and am redirected to the admin dashboard page
#
 Scenario: User tries to signup using an existing user name.
   Given I am on signup page
   When I submit existing username in the signup page
   Then I see an error message and I am on the signup page

#  # TODO: Need to add when email address is used as username.
#  #  Scenario: User enters an incorrect value for username on the signup page and is unable to create an account.
#  #   Given I am on signup page
#  #   When I submit an invalid username and a valid password in the signup page
#  #   Then I see an error message and I am on the signup page
#
  Scenario: User enters an incorrect value for incorrect passwords on the signup page and is unable to create an account.
   Given I am on signup page
   When I submit a valid username and incorrect passwords in the signup page
   Then I see an error message and I am on the signup page

  Scenario: User enters an invalid password on the signup page and is unable to create an account.
   Given I am on signup page
   When I submit a valid username and an invalid password in the signup page
   Then I see an error message and I am on the signup page

  Scenario: User leaves the username field empty on the signup page and is unable to create an account.
   Given I am on signup page
   When I leave the username field empty and submit a valid password in the signup page
   Then I see an error message and I am on the signup page

  Scenario: User leaves both the password fields empty on the signup page and is unable to create an account.
   Given I am on signup page
   When I leave both the password fields empty and submit a valid username in the signup page
   Then I see an error message and I am on the signup page

  Scenario: User leaves one of the password fields empty on the signup page and is unable to create an account.
   Given I am on signup page
   When I leave one of the password fields empty and submit a valid username in the signup page
   Then I see an error message and I am on the signup page

##    TODO:
##    Scenario: When an user enters a duplicate username and valid passwords on the signup page, the user's request is rejected.
#