# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class Aspire360Survey(models.Model):
#     _name = 'survey.survey'
#     _inherit = 'survey.survey'
#     _description = 'Aspire360 Survey'

    # entrepreneur = fields.Many2One('aspire360.entrepreneurs', 'name',required=True)

class Entrepreneurs(models.Model):
    _name = 'aspire360.entrepreneurs'

    name = fields.Char()
    surveys = fields.Html()
    # surveys = One2many('aspire360.entrepreneurs','entrepreneur',require=True)

class VentureCapitalists(models.Model):
    _name = 'aspire360.venturecapitalists'

    name = fields.Char()
    followed_companies = fields.Html()
    # followed_companies = fields.One2many('aspire360.entrepreneurs',).


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
