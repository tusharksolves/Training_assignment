from odoo import api, fields, models
from datetime import date
from odoo.exceptions import ValidationError
from datetime import datetime, time
import logging
_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Master'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True, tracking=True)
    dob = fields.Date(string="Date of Birth", required=True, tracking=True)
    age = fields.Integer(string="Age", compute='_compute_age', store=True, tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender",required=True, tracking=True)
    # disease = fields.Char(string="Diseases", required=True)
    email = fields.Char(string="Email Address",required=True, tracking=True)
    phone = fields.Char(string="Phone Number",required=True, tracking=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments", tracking=True)
    user_id = fields.Many2one('res.users', string="Related User", required=False, tracking=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Assigned Doctor", tracking=True)
    # Many2many relationship to diseases
    disease_ids = fields.Many2many(
        'hospital.disease',
        'patient_disease_rel',
        'patient_id',
        'disease_id',
        string='Diseases',
        tracking=True
    )
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)



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


    @api.model
    def create(self, vals):
        patient = super().create(vals)

        email = vals.get('email')
        name = vals.get('name')
        password = vals.get('password', 'patient123')

        if email:
            user = self.env['res.users'].sudo().create({
                'name': name,
                'login': email,
                'email': email,
                'password': password,
            })

            patient.sudo().user_id = user.id

        return patient

    def action_book_appointment(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'Book Appointment',
            'res_model': 'hospital.appointment',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
            }
        }
    def action_open_cancel_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment.cancel.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
            }
        }


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_id = fields.Many2one('hospital.patient', string="Patient Name", required=True, tracking=True)
    appointment_date = fields.Datetime(string="Appointment Date", required=True, tracking=True)
    # notes = fields.Text(string="Notes")
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True, tracking=True)

    cancel_reason = fields.Text(string='Cancellation Reason', tracking=True)


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


    @api.model
    def send_daily_appointment_emails(self):
        f

        _logger.info("🔁 Running send_daily_appointment_emails()")

        today = date.today()
        _logger.info(f"🔍 Today's date: {today}")

        start_of_day = datetime.combine(today, time.min)
        end_of_day = datetime.combine(today, time.max)

        appointments = self.search([
            ('appointment_date', '>=', start_of_day),
            ('appointment_date', '<=', end_of_day),
        ])

        _logger.info(f"📝 Appointments found: {len(appointments)}")

        # Group appointments by doctor
        doctor_dict = {}
        for appt in appointments:
            if appt.doctor_id and appt.doctor_id.email:
                doctor_dict.setdefault(appt.doctor_id, []).append(appt)

        # Send email to each doctor
        for doctor, appts in doctor_dict.items():
            patient_names = "\n".join(
                f"- {appt.patient_id.name}" for appt in appts if appt.patient_id
            )
            email_body = f"Dear Dr. {doctor.name},\n\nYou have the following appointments today:\n\n{patient_names}\n\nRegards,\nHospital Team"

            self.env['mail.mail'].create({
                'subject': 'Today\'s Appointments',
                'body_html': f'<pre>{email_body}</pre>',
                'email_to': doctor.email,
            }).send()

    @api.model
    def create(self, vals):
        appointment = super().create(vals)

        if appointment.patient_id:
            appointment.patient_id.status = 'confirmed'

        return appointment


