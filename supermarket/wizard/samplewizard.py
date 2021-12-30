# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SampleWizard(models.TransientModel):
    _name = 'create.sample.wizard'
    _description = 'create sample wizard'

    name = fields.Char(string='Name')
    def submit(self):
        for record in self:
            record.create({
                'name':'SathisKana'
            })
