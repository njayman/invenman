from odoo import models, fields, api

class ProductLot(models.Model):
    _name = 'invenman.product_lot'
    _description = 'Product Lots (Purchases)'
    
    name = fields.Char(string="Lot Name", required=True, copy=False, default="New")
    product_id = fields.Many2one('invenman.product', string="Product", required=True)
    supplier_id = fields.Many2one('invenman.supplier', string="Supplier", required=True)
    
    quantity = fields.Float(string="Purchased Quantity", required=True)
    unit_id = fields.Many2one('invenman.unit', string="Unit", required=True)
    purchase_price = fields.Float(string="Purchase Price", required=True)
    
    sale_price = fields.Float(string="Sale Price")  # Default sale price per unit
    sold_quantity = fields.Float(string="Sold Quantity", compute="_compute_sold_quantity", store=True)
    available_quantity = fields.Float(string="Available Quantity", compute="_compute_available_quantity", store=True)
    sale_ids = fields.One2many('invenman.sale.line', 'lot_id', string="Sales")

    sold_quantity = fields.Float(
        string="Sold Quantity",
        compute="_compute_sold_quantity",
        store=True
    )

    available_quantity = fields.Float(
        string="Available Quantity",
        compute="_compute_available_quantity",
        store=True
    )

    @api.depends('sale_ids.quantity')
    def _compute_sold_quantity(self):
        for record in self:
            record.sold_quantity = sum(record.sale_ids.mapped('quantity'))

    @api.depends('quantity', 'sold_quantity')
    def _compute_available_quantity(self):
        for record in self:
            record.available_quantity = record.quantity - record.sold_quantity