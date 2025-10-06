from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    note = fields.Char(string="Notes")
    custom_order_line_ids = fields.One2many(
        'custom.order.line', 'order_id', string="Custom Order Lines"
    )

    def action_copy_sale_lines_to_custom(self):
        for order in self:
            # order.custom_order_line_ids.unlink()  # Clear previous custom lines if needed
            for line in order.order_line:
                self.env['custom.order.line'].create({
                    'order_id': order.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'qty_delivered': line.qty_delivered,
                    'qty_invoiced': line.qty_invoiced,
                    'price_subtotal': line.price_subtotal,

                })

    def action_open_custom_line_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Custom Order Line Wizard',
            'res_model': 'custom.order.line.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sale_order_id': self.id,
            }
        }


class CustomOrderLine(models.Model):
    _name = 'custom.order.line'
    _description = 'Custom Order Line'

    order_id = fields.Many2one('sale.order', string="Order Reference", required=True)
    product_id = fields.Many2one('product.product', string="Product")
    # product_id = fields.Char(string="Product")
    product_uom_qty = fields.Float(string="Quantity")
    price_unit = fields.Float(string="Unit Price")
    qty_delivered = fields.Float(string="Delivered")
    qty_invoiced = fields.Float(string="Invoiced")
    price_subtotal = fields.Float(string="Amount")

