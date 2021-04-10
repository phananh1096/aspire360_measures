# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
<<<<<<< Updated upstream
=======
from socket import *
import base64
import time

# Validation parameter. Turn off when developing and on when testing
VALIDATION = True
>>>>>>> Stashed changes

class Aspire360(http.Controller):
    @http.route('/aspire360measures/', auth='public',website=True)
    def index(self, **kw):
        # entrepreneurs = http.request.env['aspire360.entrepreneurs']
        # venture_capitalists = http.request.env['aspire360.venturecapitalists']
        entrepreneurs = http.request.env['aspire360.entrepreneurs'].search([('user_id', '=', request.env.context.get ('uid'))])
        venture_capitalists = http.request.env['aspire360.venturecapitalists'].search([('user_id', '=', request.env.context.get ('uid'))])
        print("Entrepreneurs: ", entrepreneurs.name)
        print("Venture capitalists: ", venture_capitalists)
        print("User uid: ", request.env.user)
        print("User uid: ",request.env.context)
        print("User uid: ", request.env.context.get ('uid'))
        print("Context: ", http.request.env['ir.config_parameter'].sudo().get_param('web.base.url'))
        # If user doesn't exist in either, redirect to create page to get them to get them to decide whether entrepreneur or vc
        if len(entrepreneurs) == 0 and len(venture_capitalists) == 0:
            print('Making changes')
            return http.request.redirect('/aspire360measures/setup')
<<<<<<< Updated upstream
        elif len(venture_capitalists) > 0:
            return http.request.render('aspire360_measures.v_index')
=======
        elif self.is_venturecapitalist():
            entrepreneurs = list()
            e_ids = venture_capitalists[0].get_entrepreneurs_followed()
            for e_id in e_ids:
                entrepreneur = http.request.env['aspire360.entrepreneurs'].search([('user_id', '=', e_id)])
                if len(entrepreneur) > 0:
                    entrepreneurs.append(entrepreneur[0])
            print(entrepreneurs)
            return http.request.render('aspire360_measures.v_index', {
                'companies': entrepreneurs
                })
>>>>>>> Stashed changes
        else:
            print('Entering entrepreneur view')
            survey_status = http.request.env['survey.user_input'].search([('survey_id', '=', 5)])
            print(survey_status)
            survey_done = survey_status[0].state
            print(survey_done)
            survey_score = survey_status[0].scoring_percentage
            print(survey_score)
            survey_date = survey_status[0].start_datetime
            return http.request.render('aspire360_measures.e_index', {'e_name':entrepreneurs.name, 'status':survey_done, 'score':survey_score, 'date': survey_date})
        # print("User uid: ", self.env.user.name)
        #TODO: Apply filter to check based on id?
        # Validation: Check if user id exists within tables. If not, redirect to setup.
        # IF record not found in both entrepreneurs and venture_capitalists: redirect to /setup

    
    @http.route('/aspire360measures/setup', auth='public',website=True)
    def setup(self, **kw):
        #Security measure to prevent someone from signing up twice
        entrepreneurs = http.request.env['aspire360.entrepreneurs'].search([('user_id', '=', request.env.context.get ('uid'))])
        venture_capitalists = http.request.env['aspire360.venturecapitalists'].search([('user_id', '=', request.env.context.get ('uid'))])
        if len(entrepreneurs) > 0 or len(venture_capitalists) > 0:
            return http.request.redirect('/aspire360measures')
        return http.request.render('aspire360_measures.setup')
    
    @http.route('/aspire360measures/setup/v', auth='public',website=True)
    def setup_e(self, **kw):
        #Security measure to prevent someone from signing up twice
        entrepreneurs = http.request.env['aspire360.entrepreneurs'].search([('user_id', '=', request.env.context.get ('uid'))])
        venture_capitalists = http.request.env['aspire360.venturecapitalists'].search([('user_id', '=', request.env.context.get ('uid'))])
        if len(entrepreneurs) > 0 or len(venture_capitalists) > 0:
            return http.request.redirect('/aspire360measures')
        else:
            # Call respective model functions to create new user
            new_record = {'name':request.env.user.name,
                          'user_id':request.env.context.get ('uid')}
            venture_capitalists.create(new_record)
        return http.request.redirect('/aspire360measures')
    

    @http.route('/aspire360measures/setup/e', auth='public',website=True)
    def setup_v(self, **kw):
        #Security measure to prevent someone from signing up twice
        entrepreneurs = http.request.env['aspire360.entrepreneurs'].search([('user_id', '=', request.env.context.get ('uid'))])
        venture_capitalists = http.request.env['aspire360.venturecapitalists'].search([('user_id', '=', request.env.context.get ('uid'))])
        if len(entrepreneurs) > 0 or len(venture_capitalists) > 0:
            return http.request.redirect('/aspire360measures')
        else:
            # Call respective model functions to create new user
            # Call respective model functions to create new user
            new_record = {'name':request.env.user.name,
                          'user_id':request.env.context.get ('uid')}
            entrepreneurs.create(new_record)
        return http.request.redirect('/aspire360measures')
        
    @http.route('/aspire360measures/survey/fundraise', auth='public', website=True)
    def survey_1(self):
        surveys = http.request.env['survey.survey'].search([('title', '=', 'Readiness to Fundraise Assessment')])
        end_url = ''
        for survey in surveys:
            user_inputs = survey._create_answer(user=request.env.user)
            user_session = user_inputs.search([])[-1]
            # print("Num user sessions is: ", len(user_inputs.search([])))
            # print("Generated Access token is: ", user_session.access_token)
            # print("Generated Access token is: ", user_session.get_start_url())
            # print("Updating survey: ", user_session.survey_id)
            # print(" with user_id: ", request.env.context.get ('uid'))
            user_session.update_entrepreneur(user_session.access_token, request.env.context.get ('uid'))
            end_url = user_session.get_start_url()
            # print("Updated record, now to test if it is actually stored")
            # # Test
        # #Check to see if record is updated:
        # updated_records = http.request.env['survey.user_input'].search([('aspire_entrepreneur', '=', request.env.context.get ('uid'))])
        # for record in updated_records:
        #     print("Survey being tested is: ", record.access_token)
        survey_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url') + end_url
        return http.request.redirect(survey_url)

    @http.route('/aspire360measures/survey/sell', auth='public', website=True)
    def survey_2(self):
        surveys = http.request.env['survey.survey'].search([('title', '=', 'Readiness to Sell Assessment')])
        end_url = ''
        for survey in surveys:
            user_inputs = survey._create_answer(user=request.env.user)
            # print("User id is: ", request.env.user)
            user_session = user_inputs.search([])[-1]
            # print("Num user sessions is: ", len(user_inputs.search([])))
            # print("Generated Access token is: ", user_session.access_token)
            # print("Generated Access token is: ", user_session.get_start_url())
            user_session.update_entrepreneur(user_session.access_token, request.env.context.get ('uid'))
            end_url = user_session.get_start_url()
        survey_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url') + end_url
        return http.request.redirect(survey_url)

<<<<<<< Updated upstream
=======
    @http.route('/aspire360measures/entrepreneur_edit_profile', auth='public',website=True)
    def entrepreneur_edit_profile(self, **kw):
        #Validate current user is entrepreneur
        if VALIDATION and not self.is_entrepreneur():
            return http.request.redirect('/aspire360measures')
        return http.request.render('aspire360_measures.entrepreneur_edit_profile')
    
    @http.route('/aspire360measures/submit_info', auth='public',website=True, csrf=False)
    def submit_info(self, **kw):
        if VALIDATION and not self.is_entrepreneur():
            return http.request.redirect('/aspire360measures')
        entrepreneurs = http.request.env['aspire360.entrepreneurs']
        entrepreneurs.edit_profile(kw, request.env.context.get ('uid'))
        print("Params are: {}".format(kw))
        # print("company name: ", kw["company_info"])

        # print("company industry: ", kw["company_industry"])
        # print("company employee: ", kw["company_employees"])
        # print("company funding: ", kw["company_funding_stage"])
        return http.request.render('aspire360_measures.e_index')
    
    @http.route('/aspire360measures/search', auth='public',website=True, csrf=False)
    def search(self, **kw):
        if VALIDATION and not self.is_venturecapitalist():
            return http.request.redirect('/aspire360measures')
        #Validate current user is venture capitalisst
        # venture_capitalists = http.request.env['aspire360.venturecapitalists'].search([('user_id', '=', request.env.context.get ('uid'))])
        # if len(venture_capitalists) == 0:
        #     return http.request.redirect('/aspire360measures')
        print("Params are: {}".format(kw))
        #TODO: UPDATE SEARCH FUNCTION BASED ON PARAMS
        params = list()
        if "company_name" in kw and kw["company_name"] != "":
            params.append(("company_name","=",kw["company_name"]))
        if "industry" in kw and kw["industry"] != "All":
            params.append(("company_industry","=",kw["industry"]))
        if "employees" in kw and kw["employees"] != "All":
            params.append(("company_size","=",kw["employees"]))
        if "funding_stage" in kw and kw["funding_stage"] != "All":
            params.append(("company_funding","=",kw["funding_stage"]))
        entrepreneurs = http.request.env['aspire360.entrepreneurs'].search(params)
        print("Num entries: ", len(entrepreneurs))
        return http.request.render('aspire360_measures.search',{
            'companies': entrepreneurs
        })

    @http.route('/aspire360measures/display_fundraise', auth='public',website=True, csrf=False)
    def display_fundraise(self, **kw):
        if VALIDATION and not self.is_venturecapitalist():
            return http.request.redirect('/aspire360measures')
        print("Params for display_fundraise are: {}".format(kw))
        survey = http.request.env['survey.survey'].search([('title', '=', 'Readiness to Fundraise Assessment')])[0]
        survey_id = survey["access_token"]
        
        latest_survey_entry = http.request.env['survey.user_input'].search([("aspire_entrepreneur","=", int(kw["user_id"])),
                                                                             ("state","=","done"),
                                                                             ("aspire_type","=","fundraise")])
        print("User_id is: ", kw["user_id"])
        print("Num Results is:", len(latest_survey_entry))
        if len(latest_survey_entry) > 0:
            latest_survey_token = latest_survey_entry[-1]["access_token"]
            survey_results_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url') + "/survey/print/" + survey_id + "?answer_token=" + latest_survey_token + "&review=False"
            # print("Num entries: ", len(entrepreneurs))
            print("link to survey is: ", survey_results_url)
            return http.request.redirect(survey_results_url)
        else:
            return http.request.render("aspire360_measures.survey_error")
    
    @http.route('/aspire360measures/display_sell', auth='public',website=True, csrf=False)
    def display_sell(self, **kw):
        if VALIDATION and not self.is_venturecapitalist():
            return http.request.redirect('/aspire360measures')
        print("Params for display_sell are: {}".format(kw))
        survey = http.request.env['survey.survey'].search([('title', '=', 'Readiness to Sell Assessment'),])[0]
        survey_id = survey["access_token"]

        latest_survey_entry = http.request.env['survey.user_input'].search([("aspire_entrepreneur","=", int(kw["user_id"])),
                                                                            ("state","=","done"),
                                                                            ("aspire_type","=","sell")])
        if len(latest_survey_entry) > 0:
            latest_survey_token = latest_survey_entry[-1]["access_token"]
            survey_results_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url') + "/survey/print/" + survey_id + "?answer_token=" + latest_survey_token + "&review=False"
            # print("Num entries: ", len(entrepreneurs))
            print("link to survey is: ", survey_results_url)
            return http.request.redirect(survey_results_url)
        else:
            return http.request.render("aspire360_measures.survey_error")

    @http.route('/aspire360measures/follow_entrepreneur', auth='public',website=True, csrf=False)    
    def follow_entrepreneur(self, **kw):
        # Check if function is entered - done
        #print('Hello from follow_entrepreneur')
        print("Params for follow_entrepreneur are: {}".format(kw))

        # Get the ID of the VC - done
        venture_capitalists = http.request.env['aspire360.venturecapitalists'].search([('user_id', '=', request.env.context.get ('uid'))])
        print('Venture Capitalist ID - ', venture_capitalists)

        # Get the ID of the entrepreneur - done
        entrepreneur_id = int(kw["user_id"])
        #entrepreneur = http.request.env['aspire360.entrepreneurs'].search([('user_id', '=', request.env.context.get ('uid'))])
        print('Entrepreneur - ', entrepreneur_id)

        # Somehow combine the two - done
        venture_capitalists.follow_entrepreneur(entrepreneur_id)        

        return http.request.redirect('/aspire360measures')


    """ --- Helper functions --- """
    # Validation helpers
    def is_entrepreneur(self):
        entrepreneurs = http.request.env['aspire360.entrepreneurs'].search([('user_id', '=', request.env.context.get ('uid'))])
        if len(entrepreneurs) > 0:
            return True
        else:
            return False
    
    def is_venturecapitalist(self):
        venture_capitalists = http.request.env['aspire360.venturecapitalists'].search([('user_id', '=', request.env.context.get ('uid'))])
        if len(venture_capitalists) > 0:
            return True
        else:
            return False


>>>>>>> Stashed changes
    # @http.route('/academy/teacher/<model("academy.teachers"):teacher>/', auth='public', website=True)
    # def teacher(self, teacher):
    #     return http.request.render('academy.biography', {
    #         'person': teacher
    #     })

# class Aspire360Measures(http.Controller):
#     @http.route('/aspire360_measures/aspire360_measures/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aspire360_measures/aspire360_measures/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('aspire360_measures.listing', {
#             'root': '/aspire360_measures/aspire360_measures',
#             'objects': http.request.env['aspire360_measures.aspire360_measures'].search([]),
#         })

#     @http.route('/aspire360_measures/aspire360_measures/objects/<model("aspire360_measures.aspire360_measures"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aspire360_measures.object', {
#             'object': obj
#         })
