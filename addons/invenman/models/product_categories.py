from odoo import models, fields

class ProductCategory(models.Model):
    _name = 'invenman.product_category'
    _description = 'invenman custom product category'
    
    name = fields.Char(string="Category Name", required=True)
    