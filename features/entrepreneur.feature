Feature: setting up a new entrepreneur

  Scenario: user wants to start and setup Aspire360 app
      Given we have odoo installed
      When we go to home screen
      Then we can go to Aspire360

  Scenario: user enters home page
      Given we have Aspire360 installed
      When we go to home screen
      Then we go to signin
      Then we log in
  
  Scenario: user fails survey
      Given we are on the home page
      When we go to surveys
      Then we go to fundraising survey
      Then we fail the survey
  
  Scenario: user passes survey
      Given we are on the home page
      When we go to surveys
      Then we go to fundraising survey
      Then we pass the survey

  Scenario: entrepreneur tries to take wrong survey
      Given we are on the home page
      When we go to surveys
      Then we go to fundraising survey
      Then we don't see the survey
    