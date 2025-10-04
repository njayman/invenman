from odoo import models, fields, api

class LotLine(models.Model):
    _name = 'invenman.lot.line'
    _description = 'Inventory Lot Line'
    
    purchase_id = fields.Many2one('invenman.purchase', string="Purchase Ref.", required=True, ondelete='cascade')
    product_id = fields.Many2one('invenman.product', string="Product", required=True)
    
    supplier_id = fields.Many2one('invenman.supplier', related='purchase_id.supplier_id', store=True, readonly=True)
    
    quantity = fields.Float(string="Purchased Quantity", required=True)
    unit_id = fields.Many2one('invenman.unit', string="Unit", required=True)
    purchase_price = fields.Float(string="Purchase Price (per unit)", required=True)
    sale_price = fields.Float(string="Sale Price (per unit)")
    
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
    sale_line_ids = fields.One2many('invenman.sale.line', 'lot_line_id', string="Sales")

    @api.depends('sale_line_ids.quantity')
    def _compute_sold_quantity(self):
        for record in self:
            record.sold_quantity = sum(record.sale_line_ids.mapped('quantity'))

    @api.depends('quantity', 'sold_quantity')
    def _compute_available_quantity(self):
        for record in self:
            record.available_quantity = record.quantity - record.sold_quantity