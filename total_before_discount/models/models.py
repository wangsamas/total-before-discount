# -*- coding: utf-8 -*-
import uuid

from itertools import groupby
from datetime import datetime, timedelta
from werkzeug.urls import url_encode

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

from odoo.tools.misc import formatLang

from odoo.addons import decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    @api.depends('order_line.price_subtotal_without_disc')
    def _amount_all_w_d(self):
        """
        Compute the total amounts of the SO without discount.
        """
        for order in self:
            amount_untaxed_without_discount = 0.0
            for line in order.order_line:
                amount_untaxed_without_discount += line.price_subtotal_without_disc
            order.update({
                'amount_untaxed_without_discount': amount_untaxed_without_discount,
            })
            
    amount_untaxed_without_discount = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all_w_d', track_visibility='onchange')
    amount_untaxed = fields.Monetary(string='Discounted Amount', store=True, readonly=True, compute='_amount_all', track_visibility='onchange')
    

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends('price_unit', 'product_uom_qty')
    def _compute_amount_before_disc(self):
        """
        Compute the amounts of the SO line without discount.
        """
        for line in self:
            subtotal_w_d = line.price_unit * line.product_uom_qty
            line.update({
                'price_subtotal_without_disc': subtotal_w_d,
            })

    price_subtotal_without_disc = fields.Monetary(compute='_compute_amount_before_disc', string='Subtotal', readonly=True, store=True)

    
class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends('invoice_line_ids.price_subtotal_without_disc')
    def _compute_amount_w_d(self):
        """
        Compute the total amounts of the SO without discount.
        """
        self.amount_untaxed_without_discount = sum(line.price_subtotal_without_disc for line in self.invoice_line_ids)
            
    amount_untaxed_without_discount = fields.Monetary(string='Untaxed Amount',
        store=True, readonly=True, compute='_compute_amount_w_d', track_visibility='always')
    amount_untaxed = fields.Monetary(string='Discounted Amount',
        store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    
class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"    
    
    @api.depends('price_unit', 'quantity')
    def _compute_amount_before_disc(self):
        """
        Compute the amounts of the SO line without discount.
        """
        for line in self:
            subtotal_w_d = line.price_unit * line.quantity
            line.update({
                'price_subtotal_without_disc': subtotal_w_d,
            })

    price_subtotal_without_disc = fields.Monetary(compute='_compute_amount_before_disc', string='Subtotal', readonly=True, store=True)

    