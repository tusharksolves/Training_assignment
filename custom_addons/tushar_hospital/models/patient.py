from odoo import api, fields, models
from datetime import date
from odoo.exceptions import ValidationError



class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Master'

    name = fields.Char(string="Name", required=True)
    dob = fields.Date(string="Date of Birth", required=True)
    age = fields.Integer(string="Age", compute='_compute_age', store=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender",required=True)
    disease = fields.Char(string="Diseases", required=True)
    email = fields.Char(string="Email Address",required=True)
    phone = fields.Char(string="Phone Number",required=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    user_id = fields.Many2one('res.users', string="Related User", required=False)
    doctor_id = fields.Many2one('hospital.doctor', string="Assigned Doctor")
    # Many2many relationship to diseases
    disease_ids = fields.Many2many(
        'hospital.disease',
        'patient_disease_rel',
        'patient_id',
        'disease_id',
        string='Diseases'
    )

    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            if rec.dob:
                today = date.today()
                born = rec.dob
                rec.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            else:
                rec.age = 0

    @api.constrains('dob')
    def _check_dob_not_in_future(self):
        for rec in self:
            if rec.dob and rec.dob > date.today():
                raise ValidationError("Enter a Valid DOB")

    def action_book_appointment(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'Book Appointment',
            'res_model': 'hospital.appointment',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_patient_id': self.id,
            }
        }
class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'

    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    appointment_date = fields.Datetime(string="Appointment Date", required=True)
    # notes = fields.Text(string="Notes")
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)


    @api.constrains('patient_id', 'doctor_id', 'appointment_date')
    def _check_same_day_appointment(self):
        for rec in self:
            if rec.patient_id and rec.doctor_id and rec.appointment_date:
                appointment_day = rec.appointment_date.date()

                duplicate = self.env['hospital.appointment'].search([
                    ('id', '!=', rec.id),
                    ('patient_id', '=', rec.patient_id.id),
                    ('doctor_id', '=', rec.doctor_id.id),
                ])

                for record in duplicate:
                    if record.appointment_date.date() == appointment_day:
                        raise ValidationError(
                            "This patient already has an appointment with this doctor on the same date."
                        )


