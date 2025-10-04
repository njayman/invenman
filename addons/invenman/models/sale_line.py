from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleLine(models.Model):
    _name = 'invenman.sale.line'
    _description = 'Sale Line'
    
    sale_id = fields.Many2one('invenman.sale', string="Sale", required=True, ondelete='cascade')
    lot_id = fields.Many2one('invenman.product_lot', string="Product Lot", required=True, ondelete='restrict')
    product_id = fields.Many2one('invenman.product', related='lot_id.product_id', store=True)
    supplier_id = fields.Many2one('invenman.supplier', related='lot_id.supplier_id', store=True)
    
    quantity = fields.Float(string="Quantity", required=True)
    purchase_price = fields.Float(string="Purchase Price", related='lot_id.purchase_price', store=True)
    sale_price = fields.Float(string="Sale Price", required=True)
    
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    @api.depends('quantity', 'sale_price')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.quantity * record.sale_price

    @api.constrains('quantity')
    def _check_quantity_available(self):
        for line in self:
            if line.quantity > line.lot_id.available_quantity:
                raise ValidationError(f"Not enough stock in {line.lot_id.name}. Available: {line.lot_id.available_quantity}")
