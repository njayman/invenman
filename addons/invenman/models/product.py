from odoo import models, fields

class Product(models.Model):
    _name = 'invenman.product'
    _description = 'invenman custom product'
    
    name = fields.Char(string="Product Name", required=True)
    description = fields.Char(string="Description")
    category_id = fields.Many2one('invenman.product_category', string="Category")
