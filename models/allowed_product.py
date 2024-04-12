# -*- coding: utf-8 -*-
from odoo import fields, models


class AllowedProduct(models.Model):
    _inherit = ['res.partner']

    allowed_product_ids = fields.Many2many('product.template',
                                           string='Allowed Product')
    product_category_ids = fields.Many2one(
        'product.public.category', string='Product Category')
