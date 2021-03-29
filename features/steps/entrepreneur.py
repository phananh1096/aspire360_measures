from behave import *
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait

use_step_matcher("re")

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "usr/local/bin/chromedriver")

chrome_path = r'/usr/local/bin/chromedriver' #path from 'which chromedriver'
driver = webdriver.Chrome(executable_path = chrome_path)

@given('we have odoo installed')
def step_impl(context):
    try:
        driver.get("http://localhost:8069")
    except:
        assert False
    assert True

@when('we go to home screen')
def step_impl(context):
    try:
        driver.get("http://localhost:8069")
        #assert "Homepage!" in driver.page_source
    except:
        assert False
    assert True

@then('we can go to Aspire360')
def step_impl(context):
    try:
        driver.get("http://localhost:8069/aspire360measures")
    except:
        assert False
    assert True

@given('we have Aspire360 installed')
def step_impl(context):
    try:
        driver.get("http://localhost:8069/aspire360measures")
    except:
        assert False
    assert True

@then('we go to signin')
def step_impl(context):
    try:
        driver.get("http://localhost:8069/web/login")
    except:
        assert False
    assert True

@then('we log in')
def step_impl(context):
    email_input = driver.find_element_by_id("login")
    email_input.send_keys('admin')
    email_input.send_keys(Keys.ENTER)
    password_input = driver.find_element_by_id("password")
    password_input.send_keys('admin')
    password_input.send_keys(Keys.ENTER)
    assert True

@given('we are on the home page')
def step_impl(context):
    try:
        driver.get("http://localhost:8069")
    except:
        assert False
    assert True

@when('we go to surveys')
def step_impl(context):
    apps = driver.find_element_by_id("oe_applications")
    apps.click()
    try:
        surveys_button = driver.find_element_by_partial_link_text("Surveys")
        surveys_button.click()
    except:
        driver.get("http://localhost:8069/web#action=147&model=survey.survey&view_type=kanban&cids=1&menu_id=102")
    assert True

@then('we go to fundraising survey')
def step_impl(context):
    try:
        driver.get("http://localhost:8069/survey/9d328807-4283-48b6-a5b6-414b3d741dae/525294be-9679-4c0f-be56-3d26d424612e")
    except:
        assert False
    assert "Readiness to Fundraise Assessment" in driver.page_source

@then('we fail the survey')
def step_impl(context):
    try:
        python_button = driver.find_element_by_class_name("o_connected_user")
        python_button.send_keys(Keys.ENTER)
        wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='wrong_answer']"))).click()
        python_button = driver.find_element_by_class_name("o_connected_user")
        python_button.send_keys(Keys.ENTER)
    #python_button.click()
    except:
        assert "Retry" in driver.page_source
    assert True

@then('we pass the survey')
def step_impl(context):
    try:
        python_button = driver.find_element_by_class_name("o_connected_user")
        python_button.send_keys(Keys.ENTER)
        wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='right_answer']"))).click()
        python_button = driver.find_element_by_class_name("o_connected_user")
        python_button.send_keys(Keys.ENTER)
    except:
        assert "Thank you!" in driver.page_source
    #python_button.click()
    assert True

@then('we don\'t see the survey')
def step_impl(context):
    assert "Readiness to Fundraise Survey" not in driver.page_source

@given('we are on the investor home page')
def step_impl(context):
    driver.get("http://localhost:8069/aspire360measures/setup/v")
    assert "Investor Homepage" in driver.page_source

@when('we go to investor home screen')
def step_impl(context):
    driver.get("http://localhost:8069/aspire360measures/setup/v")
    assert "Investor Homepage" in driver.page_source

@then('we see investor actions')
def step_impl(context):
    #driver.get("http://localhost:8069/aspire360measures/setup")
    assert "Email Entrepreneurs" in driver.page_source

@when('we go to email screen')
def step_impl(context):
    driver.get("http://localhost:8069/aspire360measures/email")
    assert "Recipient" in driver.page_source

@then('we fill out the email template incorrectly')
def step_impl(context):
    email_input = driver.find_element_by_id("email_recipient")
    email_input.send_keys('invalid email')
    email_input = driver.find_element_by_id("email_sender")
    email_input.send_keys('investor@investor.com')
    email_input = driver.find_element_by_id("email_subject")
    email_input.send_keys('I would like to connect with you')
    email_input.send_keys(Keys.ENTER)
    assert "Invalid email" in driver.page_source

@then('we fill out the email template correctly')
def step_impl(context):
    email_input = driver.find_element_by_id("email_recipient")
    email_input.send_keys('entrepreneur@entrepreneur.com')
    email_input = driver.find_element_by_id("email_sender")
    email_input.send_keys('investor@investor.com')
    email_input = driver.find_element_by_id("email_subject")
    email_input.send_keys('I would like to connect with you')
    email_input.send_keys(Keys.ENTER)
    assert "Your email has been sent" in driver.page_source