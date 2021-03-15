# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import *
from odoo.tests import common, tagged
from odoo import _
from odoo import http
from odoo.http import request
# from odoo.addons.survey.tests import common

class TestModelA(common.TransactionCase):
    print(" IN TESTING TEST MODEL A FROM ASPIRE360")
    
    # Test 1: Check Odoo res user to make sure that unique ID is intact after install
    @tagged('-standard','aspire360')
    def test_assert_unique_uid_at_installation(self):
        print("In test_assert_unique_uid_at_installation test")
        uid = self.uid
        print("Testing uid is: ", uid)
        print("Odoo user uid is: ", request.env.context.get ('uid'))
        record = self.env['res.users'].search([('id', '=', request.env.context.get ('uid'))])
        # Check that uid created is unique
        self.assertEqual(len(record),1)

    # Test 2: Ran at initial install. Checks to make sure that user doesn't already exist in entrepreneur or VC
    @tagged('-standard', 'aspire360')
    def test_assert_no_entrepreneur_or_vc_entry_at_installation(self):
        print("In test_assert_no_entrepreneur_or_vc_entry_at_installation")
        check_entrepreneur = self.env['aspire360.entrepreneurs'].search([])
        check_vc = self.env['aspire360.venturecapitalists'].search([])
        if len(check_entrepreneur) == 0 and len(check_vc) == 0:
            #Check that no survey entrey associated
            num_surveys = self.env['survey.user_input'].search([('aspire_entrepreneur', '=', request.env.context.get ('uid'))])
            if self.assertEqual(len(num_surveys),0):
                print("Passed test: test_assert_no_entrepreneur_or_vc_entry_at_installation!!")
        else:
            self.assertTrue(True)

    # Test 3: Assert that assigned Entrepreneurs for surveys actually exist
    @tagged('-standard', 'aspire360')
    def test_assert_survey_entrepreneur_exists(self):
        print("In test_assert_survey_entrepreneur_exists")
        records = self.env ['survey.user_input'].search([('aspire_entrepreneur', '=', request.env.context.get ('uid'))])
        if len(records) > 0:
            check_entrepreneur = self.env['aspire360.entrepreneurs'].search([('user_id', '=', request.env.context.get ('uid'))])
            self.assertEqual(len(check_entrepreneur),1)
        #TODO: Update many2many relationfields for testing
        self.assertTrue(True)

    # Test 4: Assert that assigned followed VCs for entrepreneurs actually exist
    @tagged('-standard', 'aspire360')
    def test_assert_vc_followed_exists(self):
        print("In test_assert_vc_followed_exists")
        #TODO: Update many2many relationfields for testing
        # Change below to grab all entrepreneurs where this exists
        # followed_entrepreneurs = self.env['aspire360.entrepreneurs'].search([('users_id', '=', request.env.context.get ('uid'))])
        # for enntrepreneur in followed_entrepreneurs:
        self.assertTrue(True)
    
    # Test 5: Assert nthat Readiness to Fundraise survey exists
    @tagged('-standard', 'aspire360')
    def test_assert_fundraise_survey_exists(self):
        print("In test_assert_fundraise_survey_exists")
        surveys = self.env['survey.survey'].search([('title', '=', 'Readiness to Fundraise Assessment')])
        num_surveys = len(surveys)
        self.assertEqual(num_surveys,1)

    # Test 6: Assert that Readiness to Fundraise survey exists
    @tagged('-standard', 'aspire360')
    def test_assert_sell_survey_exists(self):
        print("In test_assert_sell_survey_exists")
        surveys = self.env['survey.survey'].search([('title', '=', 'Readiness to Sell Assessment')])
        num_surveys = len(surveys)
        self.assertEqual(num_surveys,1)

    # print("{} tests completed, {} tests passed.".format(test_count, test_passed))

    # test_assert_unique_uid_at_installation()