from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Supplier(models.Model):
    _name = 'invenman.supplier'
    _description = 'invenman suppliers'
    
    name = fields.Char(string="Supplier Name", required=True)
    organization = fields.Char(string="Organization")
    contact_no = fields.Char(string="Contact number")
    address = fields.Char(string="Address")
    nid = fields.Char(string="NID", required=True)

    _sql_constraints = [('unique_supplier_nid', 'unique(nid)', 'NID must be unique among suppliers.')]

    @api.constrains('nid')
    def _check_unique_nid_across_models(self):
        for record in self:
            if not record.nid:
                continue

            customer = self.env['invenman.customer'].search([('nid', '=', record.nid)], limit = 1)
            
            if customer:
                raise ValidationError(f"NID {record.nid} already exists in Customers.")