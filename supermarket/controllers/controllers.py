# -*- coding: utf-8 -*-
# from odoo import http


# class Supermarket(http.Controller):
#     @http.route('/supermarket/supermarket/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/supermarket/supermarket/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('supermarket.listing', {
#             'root': '/supermarket/supermarket',
#             'objects': http.request.env['supermarket.supermarket'].search([]),
#         })

#     @http.route('/supermarket/supermarket/objects/<model("supermarket.supermarket"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('supermarket.object', {
#             'object': obj
#         })
