# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Aspire360Survey(models.Model):
    _name = 'survey.user_input'
    _inherit = 'survey.user_input'
    _description = 'Aspire360 Extension of Surveys module'

    #Fields
    aspire_entrepreneur = fields.Many2one('res.users', string='Entrpreneur or Company', ondelete='cascade', required=False)
    # aspire_entrepreneur = fields.Many2one('aspire360.entrepreneurs', string='Entrpreneur or Company', ondelete='cascade', required=False)
    
    # Method to update survey with entrepreneur id
    def update_entrepreneur(self, access_token, entrepreneur_id):
        # Fetch records
        #TODO: Make sure search matches
        records = self.env ['survey.user_input'].search([('access_token', '=', access_token)])
        # count = 0
        for record in records:
            record.aspire_entrepreneur = entrepreneur_id
        #     count += 1
        # print("Total records updated: ", count)
        # return super(Aspire360Survey,self).write({'aspire_entrepreneur':entrepreneur_id})

class Entrepreneurs(models.Model):
    _name = 'aspire360.entrepreneurs'
    _description = 'Aspire360 Model for Entrepreneurs'

    # Fields
    name = fields.Char('User Name', help='User Name associated with Odoo Res_user', readonly=True)
    user_id = fields.Integer('User ID', help='User ID associated with Odoo Res_user', readonly=True)
    # Relation Fields
    surveys = fields.One2many('survey.user_input',string='Linked_survey_entry', inverse_name='aspire_entrepreneur', required=False)
    investors = fields.Many2many('aspire360.venturecapitalists', string='Investor', ondelete='cascade', required=False)

    # Add a survey associated with Entrepreneur
    @api.model
    def create(self, vals):
        return super(Entrepreneurs, self).create(vals)
    
    # Add a survey associated with Entrepreneur
    def update_investor(self, entrepreneur_id, investor_id):
        #TODO: Create function
        return

class VentureCapitalists(models.Model):
    _name = 'aspire360.venturecapitalists'
    _description = 'Aspire360 Model for Investors'

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
