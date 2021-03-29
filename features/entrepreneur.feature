Feature: setting up and using core features of Aspire360

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

  Scenario: investor tries to take wrong survey
      Given we are on the home page
      When we go to surveys
      Then we go to fundraising survey
      Then we don't see the survey

  Scenario: Investor enters home page
      Given we have Aspire360 installed
      When we go to investor home screen
      Then we see investor actions

  Scenario: Investor tries to contact an entrepreneur they haven't matched with
      Given we are on the investor home page
      When we go to email screen
      Then we fill out the email template incorrectly

  Scenario: Investor tries to contact an entrepreneur they have matched with
      Given we are on the investor home page
      When we go to email screen
      Then we fill out the email template correctly
    