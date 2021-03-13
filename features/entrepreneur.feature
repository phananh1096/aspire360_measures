Feature: setting up a new entrepreneur

  Scenario: create an entrepreneur
     Given we have Aspire360 installed
      When we create a new entrepreneur
      Then the entrepreneur should have a name
      Then the entrepreneur should have a user_id
      Then the entrepreneur should not have surveys
      Then the entrepreneur should not have investors