from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleLine(models.Model):
    _name = 'invenman.sale.line'
    _description = 'Sale Line'
    
    sale_id = fields.Many2one('invenman.sale', string="Sale", required=True, ondelete='cascade')
    product_id = fields.Many2one('invenman.product', string="Product", required=True)

    lot_line_id = fields.Many2one('invenman.lot.line', string="Product Lot/Batch", required=True, ondelete='restrict', 
                                  domain="[('product_id', '=', product_id), ('available_quantity', '>', 0)]")
    supplier_id = fields.Many2one('invenman.supplier', related='lot_line_id.supplier_id', store=True, readonly=True)
    purchase_price = fields.Float(string="Purchase Price", related='lot_line_id.purchase_price', store=True, readonly=True)
    
    quantity = fields.Float(string="Quantity", required=True)
    sale_price = fields.Float(string="Sale Price", required=True)
    
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    @api.depends('quantity', 'sale_price')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.quantity * record.sale_price

    @api.constrains('quantity')
    def _check_quantity_available(self):
        for line in self:
            if line.quantity > line.lot_line_id.available_quantity:
                raise ValidationError(f"Not enough stock for {line.product_id.name} (Lot: {line.lot_line_id.purchase_id.name}). Available: {line.lot_line_id.available_quantity}")