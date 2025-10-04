from odoo import models, fields, api

class Purchase(models.Model):
    _name = 'invenman.purchase'
    _description = 'Product Purchases (Header)'

    name = fields.Char(string="Purchase Reference", compute="_compute_purchase_name", store=True, readonly=False)
    supplier_id = fields.Many2one('invenman.supplier', string="Supplier", required=True)
    purchase_date = fields.Datetime(string="Purchase Date", default=fields.Datetime.now)
    lot_line_ids = fields.One2many('invenman.lot.line', 'purchase_id', string="Products Received")

    @api.depends('supplier_id', 'purchase_date')
    def _compute_purchase_name(self):
        """Generates the name as 'Supplier Name - MM-DD-YYYY'"""
        for record in self:
            if record.supplier_id and record.purchase_date:
                # Format: Supplier Name - MM-DD-YYYY
                date_str = fields.Datetime.from_string(record.purchase_date).strftime('%m-%d-%Y')
                record.name = f"{record.supplier_id.name} - {date_str}"
            elif not record.name:
                 # Provide a default name if fields are not yet set
                 record.name = "New Purchase"