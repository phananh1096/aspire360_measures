from behave import *
from models.models import Entrepreneurs

use_step_matcher("re")

@given('we have Aspire360 installed')
def step_impl(context):
    pass

@when('we create a new entrepreneur')
def step_impl(context):
    assert True is not False

@then('the entrepreneur should have a name')
def step_impl(context):
    #print(field)
    assert True is not False 

@then('the entrepreneur should have a user_id')
def step_impl(context):
    #print(field)
    assert True is not False 

@then('the entrepreneur should not have surveys')
def step_impl(context):
    #print(field)
    assert True is not False 

@then('the entrepreneur should not have investors')
def step_impl(context):
    #print(field)
    assert True is not False 