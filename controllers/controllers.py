# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from socket import *
import base64
import time

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

    @http.route('/aspire360measures/email', auth='public',website=True)
    def setup_email(self, **kw):
        #Security measure to prevent someone from signing up twice
        return http.request.render('aspire360_measures.email_form')
        
    def email_helper(self, rec, fro, msg, subj):
        endmsg = "\r\n.\r\n"
        mailserver = ("smtp.mailtrap.io", 2525)
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect(mailserver)
        clientSocket.settimeout(None)
        recv = clientSocket.recv(1024)
        recv = recv.decode()
        print(recv)
        if recv[:3] != '220':
            print('reply not received from server.')
        heloCommand = 'EHLO Alice\r\n'
        clientSocket.send(heloCommand.encode())
        recv1 = clientSocket.recv(1024)
        recv1 = recv1.decode()
        print("1: " + recv1)
        if recv1[:3] != '250':
            print('250 reply not received from server.')

        #Info for username and password
        username = "404819e151fafc"
        password = "3f6871122cd6fa"
        Authentication = 'AUTH LOGIN\r\n'
        clientSocket.send(Authentication.encode())
        recv = clientSocket.recv(1024)
        uname = base64.b64encode(username.encode()) + b'\r\n'
        clientSocket.send(uname)
        recv = clientSocket.recv(1024)
        uname = base64.b64encode(password.encode()) + b'\r\n'
        clientSocket.send(uname)
        recv = clientSocket.recv(1024)

        command = "MAIL FROM:<" + fro + ">\r\n"
        clientSocket.send(str.encode(command))
        recv2 = clientSocket.recv(1024)
        recv2 = recv2.decode()

        command = "RCPT TO:<" + rec + ">\r\n"
        clientSocket.send(str.encode(command))
        recv3 = clientSocket.recv(1024)
        recv3 = recv3.decode()

        command = "DATA\r\n"
        clientSocket.send(str.encode(command))
        recv4 = clientSocket.recv(1024)
        recv4 = recv4.decode()

        command = "Subject: " + subj + "\r\n\r\n" 
        clientSocket.send(str.encode(command))
        date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
        date = date + "\r\n\r\n"
        clientSocket.send(str.encode(date))
        clientSocket.send(str.encode(msg))
        clientSocket.send(str.encode(endmsg))
        recv_msg = clientSocket.recv(1024)

        quit = "QUIT\r\n"
        clientSocket.send(str.encode(quit))
        recv5 = clientSocket.recv(1024)
        print(recv5)
        clientSocket.close()

    @http.route('/aspire360measures/submit_email', auth='public',website=True, csrf=False)
    def submit_email(self, **kw):
        print("Params are: {}".format(kw))
        # print("company name: ", kw["company_info"])

        # print("company industry: ", kw["company_industry"])
        # print("company employee: ", kw["company_employees"])
        # print("company funding: ", kw["company_funding_stage"])
        #return http.request.render('aspire360_measures.e_index')
        msg = ""
        if kw["email_template"] == "Follow-up":
            msg = "This is a follow-up from the investor. This is a test message for development"
        else:
            msg = "This is an introduction from the investor. This is a test message for development"
        self.email_helper(kw["email_recipient"], kw["email_sender"], msg, kw["email_template"])

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
            user_session.update_entrepreneur(user_session.access_token, request.env.context.get ('uid'), "fundraise")
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
            print("Generated Access token is: ", user_session.access_token)
            # print("Generated Answer token is: ", user_session.answer_token)
            # print("Generated Access token is: ", user_session.get_start_url())
            user_session.update_entrepreneur(user_session.access_token, request.env.context.get ('uid'),"sell")
            end_url = user_session.get_start_url()
        survey_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url') + end_url
        return http.request.redirect(survey_url)

    @http.route('/aspire360measures/entrepreneur_form', auth='public',website=True)
    def entrepreneur_form(self, **kw):
        return http.request.render('aspire360_measures.entrepreneur_form')
    
    @http.route('/aspire360measures/submit_info', auth='public',website=True, csrf=False)
    def submit_info(self, **kw):
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
        print("Params are: {}".format(kw))
        #TODO: UPDATE SEARCH FUNCTION BASED ON PARAMS
        params = list()
        if "company_name" in kw and kw["company_name"] != "":
            params.append(("company_name","=",kw["company_name"]))
        if "company_industry" in kw and kw["company_industry"] != "All":
            params.append(("company_industry","=",kw["company_industry"]))
        if "company_size" in kw and kw["company_size"] != "All":
            params.append(("company_size","=",kw["company_size"]))
        if "company_funding" in kw and kw["company_funding"] != "All":
            params.append(("company_funding","=",kw["company_funding"]))
        entrepreneurs = http.request.env['aspire360.entrepreneurs'].search(params)
        print("Num entries: ", len(entrepreneurs))
        return http.request.render('aspire360_measures.search',{
            'companies': entrepreneurs
        })

    @http.route('/aspire360measures/display_fundraise', auth='public',website=True, csrf=False)
    def display_fundraise(self, **kw):
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
