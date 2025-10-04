from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Sale(models.Model):
    _name = 'invenman.sale'
    _description = 'Product Sales'
    
    name = fields.Char(string="Sale Reference", compute="_compute_sale_name", store=True, readonly=False)
    customer_id = fields.Many2one('invenman.customer', string="Customer", required=True, ondelete='restrict') 
    sale_date = fields.Datetime(string="Sale Date", default=fields.Datetime.now)
    line_ids = fields.One2many('invenman.sale.line', 'sale_id', string="Sale Lines")
    total_amount = fields.Float(string="Total Amount", compute="_compute_total", store=True)

    payment_ids = fields.One2many('invenman.payment', 'sale_id', string='Payments')
    paid_amount = fields.Float(string="Amount Paid", compute="_compute_payment_totals", store=True)
    due_amount = fields.Float(string="Due Amount", compute="_compute_payment_totals", store=True)
    
    payment_status = fields.Selection([
        ('full', 'Fully Paid'),
        ('partial', 'Partial Payment'),
        ('due', 'Fully Due'),
    ], string='Payment Status', compute="_compute_payment_totals", store=True, default='due')
    
    initial_paid_amount = fields.Float(string="Initial Payment Amount")

    customer_total_due = fields.Float(
        string="Customer Total Due",
        related='customer_id.total_due_amount',
        readonly=True,
    )
    
    customer_recent_sales_ids = fields.Many2many(
        'invenman.sale', 
        compute='_compute_customer_recent_sales', 
        string='Recent Sales'
    )

    # ADDED: Non-stored field for controlling the transaction filter in the side preview
    show_due_only = fields.Boolean(default=False, string="Show Due Only")

    @api.depends('line_ids.subtotal')
    def _compute_total(self):
        for record in self:
            record.total_amount = sum(record.line_ids.mapped('subtotal'))

    @api.depends('total_amount', 'payment_ids.amount')
    def _compute_payment_totals(self):
        for record in self:
            total_paid = sum(record.payment_ids.mapped('amount'))
            record.paid_amount = total_paid
            
            record.due_amount = record.total_amount - total_paid
            
            if record.due_amount <= 0.01:
                record.payment_status = 'full'
            elif total_paid > 0:
                record.payment_status = 'partial'
            else:
                record.payment_status = 'due'
    
    @api.depends('customer_id')
    def _compute_customer_recent_sales(self):
        """Computes the last 5 sales for the selected customer, excluding the current sale."""
        for sale in self:
            sale.customer_recent_sales_ids = False
            if sale.customer_id:
                # Search for all sales for this customer, ordered by date descending
                all_recent_sales = self.search([
                    ('customer_id', '=', sale.customer_id.id),
                ], order='sale_date DESC')
                
                recent_sales = all_recent_sales - sale
                
                sale.customer_recent_sales_ids = [(6, 0, recent_sales[:5].ids)]

    # FIX: Add this onchange to ensure the computed field runs and the UI refreshes
    @api.onchange('customer_id')
    def _onchange_customer_preview(self):
        """Forces the update of the computed customer_recent_sales_ids when the customer is selected."""
        if self.customer_id:
            # Explicitly call the compute method. This is essential for non-stored m2m/o2m fields on new records.
            self._compute_customer_recent_sales()
            # The related field customer_total_due should refresh automatically via the related field mechanism,
            # but is displayed here for completeness.
        else:
            # Clear the transient value if no customer is selected
            self.customer_recent_sales_ids = False
    
    @api.depends('customer_id', 'sale_date')
    def _compute_sale_name(self):
        for record in self:
            customer_name = record.customer_id.name
            if customer_name and record.sale_date:
                date_obj = fields.Datetime.from_string(record.sale_date) if isinstance(record.sale_date, str) else record.sale_date
                    
                if date_obj:
                    date_str = date_obj.strftime('%m-%d-%Y')
                    record.name = f"{customer_name} - {date_str}"
                elif not record.name:
                    record.name = "New Sale"
            elif not record.name or record.name == "New":
                 record.name = "New Sale"

    @api.model
    def create(self, vals):
        initial_paid_amount = vals.pop('initial_paid_amount', 0.0)
        
        record = super(Sale, self).create(vals)
        
        if initial_paid_amount > 0:
            self.env['invenman.payment'].create({
                'sale_id': record.id,
                'amount': initial_paid_amount,
                'payment_date': fields.Datetime.now(),
            })
        
        return record