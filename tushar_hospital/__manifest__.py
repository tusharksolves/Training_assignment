{
    "name": "Hospital Management System",
    "author": "Tushar Karma",
    "category": "Hospital",
    "depends": ['base','sale', 'mail'],
    "licence":"LGPL-3",
    "data":[
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'wizard/cancel_appointment_view.xml',
        'wizard/custom_order_wizard_view.xml',
        'views/custom_login.xml',
        'views/patient_portal_template.xml',
        'views/patient_views.xml',
        'views/hospital_appointment_view.xml',
        'views/doctor_views.xml',
        'views/view_order_form.xml',
        'views/hospital_action.xml',
        'views/menu.xml',
        'data/appointment_cron.xml',

        'report/report_view.xml',
        'report/report_template.xml',
    ],
    "controllers": [
        'controller/main.py',
    ],
    'installable': True,
    'application': True,

}