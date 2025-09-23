from odoo import models, fields, api
from odoo.exceptions import UserError


class AppointmentCancelWizard(models.TransientModel):
    _name = 'hospital.appointment.cancel.wizard'
    _description = 'Cancel Appointment Wizard'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment', required=True)
    cancel_reason = fields.Text(string='Reason for Cancellation', required=True)

    def action_cancel(self):
        self.ensure_one()
        if not self.appointment_id:
            raise UserError("No appointment selected to cancel.")

        self.appointment_id.unlink()

        return {'type': 'ir.actions.act_window_close'}
