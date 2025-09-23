# models/doctor.py
from odoo import models, fields

class Doctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor Master'

    name = fields.Char(string="Name", required=True)
    specialization = fields.Char(string="Specialization")
    doctor_type = fields.Selection([
        ('children', "Children's Doctor"),
        ('general', "General Doctor")
    ], string="Doctor Type", required=True, default='general')
    patient_ids = fields.One2many('hospital.patient', 'doctor_id', string="Patients")
    appointment_ids = fields.One2many(
        'hospital.appointment', 'doctor_id', string="Appointments"
    )
    user_id = fields.Many2one('res.users', string="Related User", required=False)


