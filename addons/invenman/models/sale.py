from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Sale(models.Model):
    _name = 'invenman.sale'
    _description = 'Product Sales'
    
    name = fields.Char(string="Sale Reference", required=True, copy=False, default="New")
    customer_id = fields.Many2one('invenman.customer', string="Customer", required=True)
    sale_date = fields.Datetime(string="Sale Date", default=fields.Datetime.now)
    line_ids = fields.One2many('invenman.sale.line', 'sale_id', string="Sale Lines")
    total_amount = fields.Float(string="Total Amount", compute="_compute_total", store=True)

    @api.depends('line_ids.subtotal')
    def _compute_total(self):
        for record in self:
            record.total_amount = sum(record.line_ids.mapped('subtotal'))
