from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Customer(models.Model):
    _name = 'invenman.customer'
    _description = 'invenman customers'
    
    name = fields.Char(string="Customer Name", required=True)
    contact_no = fields.Char(string="Contact number")
    address = fields.Char(string="Address")
    nid = fields.Char(string="NID", required=True)
    
    # New computed field for total due amount
    sale_ids = fields.One2many('invenman.sale', 'customer_id', string="Sales")
    total_due_amount = fields.Float(
        string="Total Due Amount", 
        compute='_compute_total_due_amount', 
        store=True,
    )

    _sql_constraints = [('unique_customer_nid', 'unique(nid)', 'NID must be unique among customers.')]

    @api.constrains('nid')
    def _check_unique_nid_across_models(self):
        for record in self:
            if not record.nid:
                continue

            supplier = self.env['invenman.supplier'].search([('nid', '=', record.nid)], limit = 1)
            
            if supplier:
                raise ValidationError(f"NID {record.nid} already exists in Suppliers.")

    @api.depends('sale_ids.due_amount')
    def _compute_total_due_amount(self):
        for customer in self:
            customer.total_due_amount = sum(customer.sale_ids.mapped('due_amount'))

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, order=None, name_get_uid=None):
        """Enables searching by Customer Name or Contact Number."""
        args = args or []
        if name:
            domain = ['|', ('name', operator, name), ('contact_no', operator, name)]
            return self._search(domain + args, limit=limit, order=order, access_rights_uid=name_get_uid)
        
        return super(Customer, self)._name_search(
            name=name, 
            operator=operator, 
            limit=limit, 
            order=order, 
        )