# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Aspire360Survey(models.Model):
    _name = 'survey.user_input'
    _inherit = 'survey.user_input'
    _description = 'Aspire360 Extension of Surveys module'

    #Fields
    aspire_type = fields.Char('Aspire Survey Type', help='Fundraise or Sell survey', readonly=True)
    aspire_entrepreneur = fields.Many2one('res.users', string='Entrpreneur or Company', ondelete='cascade', required=False)
    # aspire_entrepreneur = fields.Many2one('aspire360.entrepreneurs', string='Entrpreneur or Company', ondelete='cascade', required=False)
    
    # Method to update survey with entrepreneur id
    def update_entrepreneur(self, access_token, entrepreneur_id, survey_type):
        # Fetch records
        #TODO: Make sure search matches
        records = self.env ['survey.user_input'].search([('access_token', '=', access_token)])
        # count = 0
        for record in records:
            record.aspire_entrepreneur = entrepreneur_id
            record.aspire_type = survey_type
        #     count += 1
        # print("Total records updated: ", count) 
        # return super(Aspire360Survey,self).write({'aspire_entrepreneur':entrepreneur_id})

class Entrepreneurs(models.Model):
    _name = 'aspire360.entrepreneurs'
    _description = 'Aspire360 Model for Entrepreneurs'
    _inherit = ['mail.thread']

    # Fields
    name = fields.Char('User Name', help='User Name associated with Odoo Res_user', readonly=True)
    user_id = fields.Integer('User ID', help='User ID associated with Odoo Res_user', readonly=True)
    # Relation Fields
    surveys = fields.One2many('survey.user_input',string='Linked_survey_entry', inverse_name='aspire_entrepreneur', required=False)
    investors = fields.Many2many('aspire360.venturecapitalists', string='Investor', ondelete='cascade', required=False)
    #
    company_name = fields.Char('Company Name', help='Company Name associated with Entrepreneur', readonly=True)
    company_industry = fields.Char('Company Industry', help='Company Industry associated with Entrepreneur', readonly=True)
    company_size = fields.Char('Company Size', help='Company Size associated with Entrepreneur', readonly=True)
    company_funding = fields.Char('Company Funding', help='Company Funding associated with Entrepreneur', readonly=True)

    # Add a survey associated with Entrepreneur
    @api.model
    def create(self, vals):
        return super(Entrepreneurs, self).create(vals)

    @api.model
    def send_email(self):
        post_vars = {'subject': "Message subject",
        'body': "Message body",
        'partner_ids': [(4, 8)],} # Where "4" adds the ID to the list 
                                # of followers and "3" is the partner ID 
        notification_ids = []
        notification_ids.append((0,0,{
            'res_partner_id':8,
            'notification_type':'inbox'}))
        self.message_post(body='This receipt has been validated!', message_type='notification', subtype='mail.mt_comment', author_id='self.env.user.partner_id.id', notification_ids=notification_ids)
    
    # Add a survey associated with Entrepreneur
    def edit_profile(self, kw, entrepreneur_id):
        print("Entrepreneur id is: ", entrepreneur_id)
        records = self.env['aspire360.entrepreneurs'].search([('user_id', '=', entrepreneur_id)])
        print("Matching records found: ", len(records))
        # Should only have 1 matching record
        for record in records:
            print("Params passed in are: ", kw)
            if "company_name" in kw:
                record.company_name = kw["company_name"]
            if "industry" in kw:
                record.company_industry = kw["industry"]
            if "employees" in kw:
                record.company_size = kw["employees"]
            if "funding_stage" in kw:
                record.company_funding = kw["funding_stage"]
        return

class DailyObjectives(models.Model):
    _name = 'aspire360.dailyobjectives'
    _description = 'Aspire360 Model for entrepreneur objectives'

    e_id = fields.Char('Entrepreneur Id', help='Id associated with Entrepreneur', readonly=True)
    objective_text = fields.Char('Objective Text', help='The actual objective', readonly=True)
    objective_status = fields.Boolean('Objective Status', help='Status of the objective')

    # Add a survey associated with Entrepreneur
    @api.model
    def create(self, vals):
        return super(DailyObjectives, self).create(vals)
    
    def get_objectives(self, e_id_arg):
        records = self.env['aspire360.dailyobjectives'].search([('e_id', '=', e_id_arg)])
        print('Records = ', records)
        return records

    def update_objectives(self, objs):
        print('Updating Objectives...')
        for obj in objs:
            records = self.env['aspire360.dailyobjectives'].search([('objective_text', '=', obj)])
            if records:
                records.objective_status = True

class VentureCapitalists(models.Model):
    _name = 'aspire360.venturecapitalists'
    _description = 'Aspire360 Model for Investors'
    _inherit = ['mail.thread']

    name = fields.Char('User Name', help='User Name associated with Odoo Res_user', readonly=True)
    user_id = fields.Integer('User ID', help='Usser ID associated with Odoo Res_user', readonly=True)
    # Relation Fields
    entrepreneur = fields.Many2many('aspire360.entrepreneurs', string='Entrpreneur or Company', ondelete='cascade', required=False)
    entrepreneurs_followed = fields.Char('Entrepreneurs Id', help='comma separated list of entrepreneurs that VC follows')
    
    # Add a survey associated with Entrepreneur
    @api.model
    def create(self, vals):
        return super(VentureCapitalists, self).create(vals)

    # Method to update survey with entrepreneur id
    def update_entrepreneur(self, investor_id, entrepreneur_id,):
        #TODO: Create function
        return
    
    @api.model
    def send_convo(self, entrepreneur, subject, content):
        # post_vars = {'subject': "Message subject",
        # 'body': "Message body",
        # 'partner_ids': [(4, 2)],} # Where "4" adds the ID to the list 
        #                         # of followers and "3" is the partner ID 
        # thread_pool = self.env['mail.thread'].search
        # self.message_post(body='This receipt has been validated!', message_type='notification', subtype_id=self.env.ref('mail.mt_comment').id, author_id=8, notification_ids=[2])
        # partners[0].message_post("Hello, how's it going?")
        # print("Channels partner_id is: ", self.env.user.partner_id.id)
        partner_id = entrepreneur.partner_id.id
        channel_id = self.env['mail.channel'].create({'name': subject, 
            'public': 'private', 
            'email_send': False, 
            'channel_partner_ids': [(4, self.env.user.partner_id.id), (4,partner_id)]})
        channel_id.message_post(
            subject=subject,
            body=content,
            message_type='notification',
            subtype_xmlid="mail.mt_comment"
        )
        # entrepreneur.notify_info(message="Message from Investor: {}".format(self.name))
        return

    def follow_entrepreneur(self, entrepreneur_id):
       # Check if you can access this function
       print('Can enter the function')
       print('Entrepreneurs followed', self.entrepreneurs_followed)
       entrepreneur_id = str(entrepreneur_id)
 
       if self.entrepreneurs_followed == False:
           self.entrepreneurs_followed = entrepreneur_id
       else:
           e_list = self.entrepreneurs_followed.split(' ')
           print(e_list)
           e_set = set(e_list)
           print(e_set)
           if entrepreneur_id in e_set:
               print('Entrepreneur already being followed')
           else:
               e_set.add(entrepreneur_id)
               new_e_list = list(e_set)
               new_string = ' '.join(new_e_list)
               self.entrepreneurs_followed = new_string
       print('Updated entrepreneurs followed', self.entrepreneurs_followed)
       return
 
    def get_entrepreneurs_followed(self):
        if self.entrepreneurs_followed == False:
            return []
        else:
            return self.entrepreneurs_followed.split(' ')

# class aspire360_measures(models.Model):
#     _name = 'aspire360_measures.aspire360_measures'
#     _description = 'aspire360_measures.aspire360_measures'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
