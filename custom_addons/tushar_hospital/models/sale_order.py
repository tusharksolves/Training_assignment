from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    note = fields.Char(string="Notes", required=True)
