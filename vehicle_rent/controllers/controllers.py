# -*- coding: utf-8 -*-
# from odoo import http


# class VehicleRent(http.Controller):
#     @http.route('/vehicle_rent/vehicle_rent/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vehicle_rent/vehicle_rent/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vehicle_rent.listing', {
#             'root': '/vehicle_rent/vehicle_rent',
#             'objects': http.request.env['vehicle_rent.vehicle_rent'].search([]),
#         })

#     @http.route('/vehicle_rent/vehicle_rent/objects/<model("vehicle_rent.vehicle_rent"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vehicle_rent.object', {
#             'object': obj
#         })
