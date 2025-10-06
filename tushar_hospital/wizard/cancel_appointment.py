from odoo import models, fields, api
from odoo.exceptions import UserError


class AppointmentCancelWizard(models.TransientModel):
    _name = 'hospital.appointment.cancel.wizard'
    _description = 'Cancel Appointment Wizard'

    # appointment_id = fields.Many2one('hospital.appointment',ondelete='cascade', string='Appointment', required=True)
    appointment_id = fields.Many2one(
        'hospital.appointment',
        string='Appointment',
        required=True,
        domain="[('patient_id', '=', patient_id)]"
    )
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)

    cancel_reason = fields.Text(string='Reason for Cancellation', required=True)


    def action_cancel(self):
        self.ensure_one()
        if not self.appointment_id:
            raise UserError("No appointment selected to cancel.")

        # Just cancel the appointment — no need to delete the wizard manually
        if self.appointment_id.patient_id:
            self.appointment_id.patient_id.status = 'cancelled'
        self.appointment_id.unlink()
        # self.patient_id.status = 'cancelled'

        return {'type': 'ir.actions.act_window_close'}


