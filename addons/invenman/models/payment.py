from odoo import models, fields, api

class Payment(models.Model):
    _name = 'invenman.payment'
    _description = 'Sale Payment Record'

    sale_id = fields.Many2one('invenman.sale', string='Sale Reference', required=True, ondelete='cascade')
    amount = fields.Float(string='Payment Amount', required=True)
    payment_date = fields.Datetime(string='Payment Date', default=fields.Datetime.now, required=True)
    customer_id = fields.Many2one(related='sale_id.customer_id', string='Customer', store=True, readonly=True)