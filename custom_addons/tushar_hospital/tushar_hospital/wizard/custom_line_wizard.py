from odoo import models, fields,api

class CustomOrderLineWizardLine(models.TransientModel):
    _name = 'custom.order.line.wizard.line'
    _description = 'Custom Order Line Wizard Line'

    wizard_id = fields.Many2one('custom.order.line.wizard', string="Wizard")
    product_id = fields.Many2one('product.product', string="Product")
    product_uom_qty = fields.Float(string="Quantity")
    price_unit = fields.Float(string="Unit Price")
    qty_delivered = fields.Float(string="Delivered")
    qty_invoiced = fields.Float(string="Invoiced")
    price_subtotal = fields.Float(string="Amount")

class CustomOrderLineWizard(models.TransientModel):
    _name = 'custom.order.line.wizard'
    _description = 'Custom Order Line Wizard'

    sale_order_id = fields.Many2one('sale.order', string="Sale Order", required=True)
    wizard_line_ids = fields.One2many(
        'custom.order.line.wizard.line', 'wizard_id', string="Wizard Lines"
    )

    @api.model
    def default_get(self, fields_list):
        res = super(CustomOrderLineWizard, self).default_get(fields_list)
        sale_order_id = self.env.context.get('default_sale_order_id')
        if sale_order_id:
            sale_order = self.env['sale.order'].browse(sale_order_id)
            lines = []
            for line in sale_order.custom_order_line_ids:
                lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'qty_delivered': line.qty_delivered,
                    'qty_invoiced': line.qty_invoiced,
                    'price_subtotal': line.price_subtotal,
                }))
            res['wizard_line_ids'] = lines
        return res

    def action_save_custom_lines(self):
        self.sale_order_id.custom_order_line_ids.unlink()  # Clear old lines

        for line in self.wizard_line_ids:
            self.env['custom.order.line'].create({
                'order_id': self.sale_order_id.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'price_unit': line.price_unit,
                'qty_delivered': line.qty_delivered,
                'qty_invoiced': line.qty_invoiced,
                'price_subtotal': line.price_subtotal,
            })