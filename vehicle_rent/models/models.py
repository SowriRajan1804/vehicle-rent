# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime


class vehicle_rent(models.Model):
    _name = 'vehicle_rent.vehicle_rent'
    _description = 'vehicle_rent.vehicle_rent'

    customer_name = fields.Many2one('res.partner',string ="Customer Name",required=True)
    payment = fields.Boolean(string="Payment")
    rent_start_date = fields.Date(string="Rent Start Date",required=True)
    rent_end_date = fields.Date(string="Rent End Date",required=True)
    vehicle_brand = fields.One2many('vehicle.details','vehicle_id')
    state =fields.Selection([('draft','Draft'),('confirm','Confirm'),('cancel','Cancel')],default='draft', string = 'Status', tracking=True)
    total = fields.Integer(string="Total Amount",compute="total_calculation")

    @api.depends('vehicle_brand.total_amount')
    def total_calculation(self):
        for order in self:
            total = 0
            for line in order.vehicle_brand:
                total += line.total_amount
            order.update({
                'total':total
            })
    @api.onchange('rent_end_date')
    def date_validation(self):
        for record in self:
            if record.rent_start_date:
                if record.rent_start_date > record.rent_end_date:
                    raise ValidationError("The rent end date must be greater then rent start date")



    def action_draft(self):
        for record in self:
            record.state = 'draft'

    def action_cancel(self):
        for record in self:
            record.state = 'cancel'

    def action_confirm(self):
        for record in self:
            record.state = 'confirm'
            for line in record.vehicle_brand:
                for vehicle in line.vehicle_number:
                    vehicle.available=False






class vehicle_name(models.Model):
    _name = 'vehicle.name'

    name=fields.Char(string="Vehicle Name")


class vehicle_details(models.Model):
    _name = 'vehicle.details'

    name = fields.Many2one('vehicle.name',string="Vehicle Name",required=True)
    vehicle_number = fields.Many2many('vehicle.info',string="Vehicle Number",domain="[('name','=',name),('available','=',True)]",required=True)
    cost = fields.Integer(string="Cost")
    start_from = fields.Char(string="Start From")
    destination = fields.Char(string="Destination")
    vehicle_id = fields.Many2one('vehicle_rent.vehicle_rent')
    quantity = fields.Integer(string="Qunty",compute='find_qty')
    tax = fields.Many2one('account.tax',string="TAX",domain=['|', ('active', '=', False), ('active', '=', True)])
    tax_amount = fields.Integer(string="Tax Amount")
    subtotal = fields.Integer(string="Subtotal",compute="get_subtotal")
    total_amount = fields.Integer(string="Total Amount")


    @api.onchange('vehicle_number')
    def find_qty(self):
        for record in self:
            count = 0
            for line in record.vehicle_number:
                count += len(line)
                record.quantity = count


    @api.onchange('quantity','tax','cost')
    def get_subtotal(self):
        for record in self:
            record.subtotal = record.cost
            record.tax_amount = record.subtotal * record.tax.amount / 100
            record.total_amount = record.subtotal + record.tax_amount

    @api.onchange('vehicle_number')
    def get_cost(self):
        for record in self:
            cost = 0
            for data in record.vehicle_number:
                cost+=data.cost
                record.cost = cost

class vehicle_information(models.Model):
    _name = 'vehicle.info'
    _rec_name ='vehicle_number'
    name = fields.Many2one('vehicle.name',string="Vehicle Name")
    vehicle_brand = fields.Many2one('vehicle.brand',string="Vehicle Brand")
    vehicle_number = fields.Char(string="Vehicle Number")
    cost = fields.Integer(string="Cost")
    available = fields.Boolean(string="Available",default=True)
    registered_city = fields.Many2one('registered.city',string ="Registered City")

class vehicle_brand(models.Model):
    _name = 'vehicle.brand'

    name = fields.Char(string="Vehicle Brand")


class registered_city(models.Model):
    _name = 'registered.city'

    name = fields.Char(string="Registered City")

class stockpicking(models.Model):
    _inherit = 'stock.picking'

    fiscal_position = fields.Many2one('account.fiscal.position',string="Fiscal Position",compute="sample")

    
    def sample(self):
        # self.fiscal_position=False
        # self.fiscal_position=self.purchase_id.fiscal_position_id
        for record in self:
            if record.purchase_id:
                for line in record.purchase_id:
                    record.fiscal_position = line.fiscal_position_id
            if record.sale_id:
                for line in record.sale_id:
                    record.fiscal_position = line.fiscal_position_id


        # test = self.env['purchase.order'].search([])
        # for i in test:
        #     if self.group_id.name == i.name:
        #         self.fiscal_position = i.fiscal_position_id

class stock_move(models.Model):
    _inherit ='stock.move'

    tax = fields.Many2one('account.tax',string="Tax",compute="compute_tax")

    def compute_tax(self):
        for record in self:
            if record.picking_id.purchase_id:
                for line in record.picking_id.purchase_id.order_line:
                    record.tax = line.taxes_id
            if record.picking_id.sale_id:
                for line in record.picking_id.sale_id.order_line:
                    record.tax = line.tax_id
            

class purchaseorder(models.Model):
    _inherit = 'purchase.order.line'

    vendar_product_code = fields.Char(string="Vendar Product Code",store=True)

    @api.onchange('product_id')
    def display_vendor_product_code(self):
        self.vendar_product_code=False
        for record in self:
            for seller_id in record.product_id.seller_ids:
                if record.partner_id.id:
                    if seller_id.name.id==record.partner_id.id:
                        record.vendar_product_code = seller_id.product_code
                else:
                    raise ValidationError("Enter the Vendor Name")


class vendorbill(models.Model):
    _inherit = 'account.move.line'

    vendar_product_code = fields.Char(string="Vendar Product Code",compute="display_vendor_product_code")


    def display_vendor_product_code(self):
        self.vendar_product_code = False
        for record in self:
            for seller_id in record.product_id.seller_ids:
                for partner_id in seller_id.name:
                    if record.partner_id.id == partner_id.id:
                       record.vendar_product_code = seller_id.product_code




