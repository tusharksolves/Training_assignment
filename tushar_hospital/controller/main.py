from odoo import http
from odoo.http import request

# class Hospital(http.Controller):
#
#     @http.route('/hospital/patient', auth='public', website=True)
#     def hospital_patient(self, **kw):
#         return "<h1>Hello from Odoo Controller!</h1>"

class Hospital(http.Controller):

    @http.route('/my/patient/dashboard', auth='user', website=True)
    def patient_dashboard(self, **kw):
        user = request.env.user
        patient = request.env['hospital.patient'].sudo().search([('user_id', '=', user.id)], limit=1)

        if patient:
            return request.render('tushar_hospital.patient_portal_template', {
                'patient': patient
            })

        else:
            return "<h1>No patient found for this user</h1>"

