# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class Academy(http.Controller):
    @http.route('/aspire360measures/', auth='public',website=True)
    def index(self, **kw):
        entrepreneurs = http.request.env['aspire360.entrepreneurs']
        venture_capitalists = http.request.env['aspire360.venturecapitalists']
        #TODO: Apply filter to check based on id?
        # Validation: Check if user id exists within tables. If not, redirect to setup.
        # IF record not found in both entrepreneurs and venture_capitalists: redirect to /setup
        return http.request.render('aspire360_measures.index')
    
    # @http.route('/aspire360measures/setup/', auth='public',website=True)
    # def setup(self, **kw):
    #     Teachers = http.request.env['academy.teachers']
    #     return http.request.render('academy.index', {
    #         'teachers': Teachers.search([])
    #     })

    @http.route('/aspire360measures/survey/fundraise', auth='public', website=True)
    def survey_1(self):
        surveys = http.request.env['survey.survey'].search([('title', '=', 'Readiness to Fundraise')])
        for survey in surveys:
            user_inputs = survey._create_answer(user=request.env.user)
            user_session = user_inputs.search([])[-1]
            print("Num user sessions is: ", len(user_inputs.search([])))
            print("Generated Access token is: ", user_session.access_token)
            print("Generated Access token is: ", user_session.get_start_url())
        return http.request.redirect(f"http://localhost:8069{user_session.get_start_url()}")

    @http.route('/aspire360measures/survey/sell', auth='public', website=True)
    def survey_2(self):
        surveys = http.request.env['survey.survey'].search([('title', '=', 'Readiness to Sell')])
        for survey in surveys:
            user_inputs = survey._create_answer(user=request.env.user)
            user_session = user_inputs.search([])[-1]
            print("Num user sessions is: ", len(user_inputs.search([])))
            print("Generated Access token is: ", user_session.access_token)
            print("Generated Access token is: ", user_session.get_start_url())
        return http.request.redirect(f"http://localhost:8069{user_session.get_start_url()}")

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
