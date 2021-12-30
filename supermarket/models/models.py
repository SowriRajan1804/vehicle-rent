# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class supermarket(models.Model):
    _name = 'supermarket.supermarket'
    _description = 'supermarket.supermarket'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string="Gender", tracking=True)
    
    # country =fields.Many2one('res.country')
    value = fields.Integer(tracking=True)
    age = fields.Integer(tracking=True)
    value2 = fields.Float(compute="_value_pc", store=True, tracking=True)
    description = fields.Text(tracking=True)
    cost_id = fields.Many2one("res.partner", string="cost", tracking=True)
    value3_ids = fields.Many2many(
        "student.student", string="value3", tracking=True)
    amount = fields.Integer(tracking=True)
    grandtotal = fields.Integer(
        compute="_Offer_calculation", store=True, default="", tracking=True)
    image = fields.Binary(string="Supermarket image")
    simple = fields.Char(string="Simple")

    @api.constrains('age')
    def SimpleCalculation(self):
        for record in self:
            if record.age < 18:
                raise ValidationError("Your not Eligible")

    @api.depends('amount')
    def _Offer_calculation(self):
        for record in self:
            if record.amount:
                if record.amount > 500:
                    record.grandtotal = int(record.amount) / 2
        return record.grandtotal

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100

    # @api.multi
    # def print_report(self):
    #     return self.env.ref('supermarket.supermarket.report_supermarket') .report_action(self)

    def submit(self):
        for record in self:
            print(record)
            print(record.value)
            # record.write({
            #     'name':'sample'
            #               })
            test = record.env['student.student'].search([])
            print(test)


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    reference = fields.Char(string="Reference")
      