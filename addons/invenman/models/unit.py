from odoo import models, fields

class Unit(models.Model):
    _name = 'invenman.unit'
    _description = 'Units of Measurement'
    
    name = fields.Char(string="Unit Name", required=True)   # e.g. "Kilogram"
    symbol = fields.Char(string="Symbol", required=True)    # e.g. "kg"
