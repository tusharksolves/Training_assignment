{
    "name": "Hospital Management System",
    "author": "Tushar Karma",
    "category": "Hospital",
    "depends": ['base','sale'],
    "licence":"LGPL-3",
    "data":[
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'wizard/cancel_appointment_view.xml',
        'views/patient_views.xml',
        'views/menu.xml',
        'views/hospital_appointment_view.xml',
        'views/doctor_views.xml',
        'views/view_order_form.xml',
        'report/report_view.xml',
        'report/report_template.xml'
    ],
    'installable': True,
    'application': True,

}