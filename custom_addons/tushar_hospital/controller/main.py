from odoo import http
from odoo.http import request

class Hospital(http.Controller):

    @http.route('/hospital/patient', auth='public', website=True)
    def hospital_patient(self, **kw):
        return "<h1>Hello from Odoo Controller!</h1>"

