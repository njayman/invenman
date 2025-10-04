from odoo import models, fields, api

class Product(models.Model):
    _name = 'invenman.product'
    _description = 'invenman custom product'
    
    name = fields.Char(string="Product Name", required=True)
    product_id_ref = fields.Char(string="Unique Product ID", required=True, copy=False, readonly=True, index=True, default=lambda self: self.env['ir.sequence'].next_by_code('invenman.product'))
    description = fields.Char(string="Description")
    category_id = fields.Many2one('invenman.product_category', string="Category")

    default_purchase_price = fields.Float(string="Default Purchase Rate")
    default_sale_price = fields.Float(string="Default Sales Rate")
    lot_line_ids = fields.One2many('invenman.lot.line', 'product_id', string="Inventory Lots")
    
    total_available_quantity = fields.Float(
        string="Total Available Quantity",
        compute="_compute_total_available_quantity",
        store=True,
    )

    @api.depends('lot_line_ids.available_quantity')
    def _compute_total_available_quantity(self):
        # Auto-update quantity: sums the available quantity from all associated lot lines
        for record in self:
            record.total_available_quantity = sum(record.lot_line_ids.mapped('available_quantity'))

    _sql_constraints = [
        ('unique_product_id_ref', 'unique(product_id_ref)', 'The Unique Product ID must be unique!'),
        ('unique_product_name', 'unique(name)', 'The Product Name must be unique!'),
    ]