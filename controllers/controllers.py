# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class Aspire360(http.Controller):
    @http.route('/aspire360measures/', auth='public',website=True)
    def index(self, **kw):
        # entrepreneurs = http.request.env['aspire360.entrepreneurs']
        # venture_capitalists = http.request.env['aspire360.venturecapitalists']
        entrepreneurs = http.request.env['aspire360.entrepreneurs'].search([('user_id', '=', request.env.context.get ('uid'))])
        venture_capitalists = http.request.env['aspire360.venturecapitalists'].search([('user_id', '=', request.env.context.get ('uid'))])
        print("Entrepreneurs: ", entrepreneurs)
        print("Entrepreneurs: ", venture_capitalists)
        print("User uid: ", request.env.user)
        print("User uid: ",request.env.context)
        print("User uid: ", request.env.context.get ('uid'))
        print("Context: ", http.request.env['ir.config_parameter'].sudo().get_param('web.base.url'))
        # If user doesn't exist in either, redirect to create page to get them to get them to decide whether entrepreneur or vc
        if len(entrepreneurs) == 0 and len(venture_capitalists) == 0:
            return http.request.redirect('/aspire360measures/setup')
        elif len(venture_capitalists) > 0:
            return http.request.render('aspire360_measures.v_index')
        else:
            return http.request.render('aspire360_measures.e_index')
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
