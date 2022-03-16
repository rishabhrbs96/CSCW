Feature: Login/Logout Page

  Scenario: Admin is able to login successfully.
    Given I am on login page
    When I submit a valid login credential
    Then I am redirected to the admin dashboard page

  Scenario: Admin is able to logout successfully.
    Given I am logged in
    When I hit the logout button
    Then I am logged out and am redirected to the home page

  Scenario: Admin enters an incorrect password and is unable to login.
    Given I am on login page
    When I submit an invalid login credential
    Then I remain on the login page
    # TODO: Can check for error message later.

  Scenario: User leaves the username field empty and hits the login button.
    Given I am on login page
    When I leave the username field blank and enter a password
    Then I remain on the login page
#    # TODO: Can check for error message later.

  Scenario: User leaves the password field empty and hits the login button.
    Given I am on login page
    When I leave the password field blank and enter an username
    Then I remain on the login page
    # TODO: Can check for error message later.

   Scenario: User enters an invalid username and is unable to login.
     Given I am on login page
     When I submit an invalid login credential
     Then I remain on the login page

  # Scenario: User is able to login.
  #   Given I am on login page
  #   When I submit a valid login credential
  #   Then I am redirected to the user dashboard page

  # Scenario: User is able to logout successfully.
  #   Given I am logged in
  #   When I hit the logout button
  #   Then I am logged out and am redirected to the login page
