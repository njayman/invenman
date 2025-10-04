from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Customer(models.Model):
    _name = 'invenman.customer'
    _description = 'invenman customers'
    
    name = fields.Char(string="Customer Name", required=True)
    contact_no = fields.Char(string="Contact number")
    address = fields.Char(string="Address")
    nid = fields.Char(string="NID", required=True)

    _sql_constraints = [('unique_customer_nid', 'unique(nid)', 'NID must be unique among customers.')]

    @api.constrains('nid')
    def _check_unique_nid_across_models(self):
        for record in self:
            if not record.nid:
                continue

            supplier = self.env['invenman.supplier'].search([('nid', '=', record.nid)], limit = 1)
            
            if supplier:
                raise ValidationError(f"NID {record.nid} already exists in Suppliers.")