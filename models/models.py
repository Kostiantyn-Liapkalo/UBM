from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    partner_type = fields.Selection([('carrier', 'Carrier'), ('supplier', 'Supplier'), ('customer', 'Customer')], string='Partner Type', required=True)

class ProductProduct(models.Model):
    _inherit = 'product.product'
    weight = fields.Float('Weight', required=True)
    volume = fields.Float('Volume', required=True)

class Order(models.Model):
    _name = 'my_product.order'
    name = fields.Char('Order Number', required=True)
    date = fields.Date('Order Date', default=fields.Date.context_today, required=True)
    supplier_id = fields.Many2one('res.partner', string='Supplier', domain=[('partner_type', '=', 'supplier')], required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', domain=[('partner_type', '=', 'customer')], required=True)
    order_lines = fields.One2many('my_product.order.line', 'order_id', string='Order Lines')
    total_amount = fields.Float(compute='_compute_totals', store=True)
    total_weight = fields.Float(compute='_compute_totals', store=True)
    total_volume = fields.Float(compute='_compute_totals', store=True)

    @api.depends('order_lines')
    def _compute_totals(self):
        for order in self:
            order.total_amount = sum(line.subtotal for line in order.order_lines)
            order.total_weight = sum(line.product_id.weight * line.quantity for line in order.order_lines)
            order.total_volume = sum(line.product_id.volume * line.quantity for line in order.order_lines)

class OrderLine(models.Model):
    _name = 'my_product.order.line'
    product_id = fields.Many2one('product.product', string='Product', required=True)
    price = fields.Float('Price', required=True)
    quantity = fields.Float('Quantity', required=True, default=1.0)
    subtotal = fields.Float(compute='_compute_subtotal', store=True)
    order_id = fields.Many2one('my_product.order', string='Order')

    @api.depends('price', 'quantity')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.price * line.quantity

class Vehicle(models.Model):
    _name = 'my_product.vehicle'
    name = fields.Char('Vehicle Number', required=True)
    carrier_id = fields.Many2one('res.partner', string='Carrier', domain=[('partner_type', '=', 'carrier')], required=True)
    max_weight = fields.Float('Maximum Weight', required=True)
    max_volume = fields.Float('Maximum Volume', required=True)

class Route(models.Model):
    _name = 'my_product.route'
    name = fields.Char('Route Name', required=True)
    carrier_id = fields.Many2one('res.partner', string='Carrier', domain=[('partner_type', '=', 'carrier')], required=True)
    vehicle_id = fields.Many2one('my_product.vehicle', string='Vehicle', required=True)
    order_ids = fields.Many2many('my_product.order', string='Orders')
    total_weight = fields.Float(compute='_compute_totals', store=True)
    total_volume = fields.Float(compute='_compute_totals', store=True)

    @api.depends('order_ids')
    def _compute_totals(self):
        for route in self:
            route.total_weight = sum(order.total_weight for order in route.order_ids)
            route.total_volume = sum(order.total_volume for order in route.order_ids)

    @api.constrains('total_weight', 'total_volume', 'vehicle_id')
    def _check_capacity(self):
        for route in self:
            if route.total_weight > route.vehicle_id.max_weight or route.total_volume > route.vehicle_id.max_volume:
                raise ValidationError('The total weight or volume of the orders exceeds the vehicle capacity.')