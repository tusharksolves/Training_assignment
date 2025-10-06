from odoo import models, fields,api

class Disease(models.Model):
    _name = 'hospital.disease'
    _description = 'Disease'

    name = fields.Char(string='Disease Name', required=True)

    # Many2many relationship to patients
    patient_ids = fields.Many2many(
        'hospital.patient',
        'patient_disease_rel',
        'disease_id',
        'patient_id',
        string='Patients'
    )