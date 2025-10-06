class DeviceType(models.Model):
    _name = 'device.type'
    _description = 'Device Type'

    name = fields.Char(required=True, unique=True)
    code = fields.Char(required=True, unique=True)
    sequence_id = fields.Many2one('ir.sequence', string='Sequence')
    device_model_ids = fields.One2many('device.model', 'device_type_id', string='Device Models')
    device_attribute_ids = fields.One2many('device.attribute', 'device_type_id', string='Attributes')
    device_ids = fields.One2many('device.device', 'device_type_id', string='Devices')

class DeviceBrand(models.Model):
    _name = 'device.brand'
    _description = 'Device Brand'

    name = fields.Char(required=True, unique=True)
    device_model_ids = fields.One2many('device.model', 'device_brand_id', string='Device Models')


class DeviceAttribute(models.Model):
    _name = 'device.attribute'
    _description = 'Device Attribute'

    name = fields.Char(required=True, unique=True)
    device_type_id = fields.Many2one('device.type', string='Device Type')
    required = fields.Boolean(default=False)
    device_attribute_value_ids = fields.One2many('device.attribute.value', 'device_attribute_id', string='Values')


class DeviceAttributeValue(models.Model):
    _name = 'device.attribute.value'
    _description = 'Device Attribute Value'

    name = fields.Char(required=True, unique=True)
    device_attribute_id = fields.Many2one('device.attribute', string='Attribute', required=True)

class DeviceModel(models.Model):
    _name = 'device.model'
    _description = 'Device Model'

    name = fields.Char(required=True, unique=True)
    device_type_id = fields.Many2one('device.type', string='Device Type', required=True)
    device_brand_id = fields.Many2one('device.brand', string='Device Brand', required=True)

class Device(models.Model):
    _name = 'device.device'
    _description = 'Device'

    name = fields.Char(string="Serial Number", required=True, unique=True)
    shared = fields.Boolean(default=False)
    device_type_id = fields.Many2one('device.type', string='Device Type', required=True)
    device_brand_id = fields.Many2one('device.brand', string='Device Brand', required=True)
    device_model_id = fields.Many2one('device.model', string='Device Model', required=True)
    attributes = fields.One2many('device.attribute.assignment', 'device_id', string='Attribute Assignments')

class DeviceAssignment(models.Model):
    _name = 'device.assignment'
    _description = 'Device Assignment'

    name = fields.Char(required=True, unique=True)
    device_id = fields.Many2one('device.device', string='Device', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    date_start = fields.Date()
    date_expire = fields.Date()
    state = fields.Selection([
        ('new', 'New'),
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('returned', 'Returned'),
        ('rejected', 'Rejected'),
    ], default='new')

class DeviceAttributeAssignment(models.Model):
    _name = 'device.attribute.assignment'
    _description = 'Device Attribute Assignment'
    _sql_constraints = [('device_attribute_unique', 'unique(device_id, device_attribute_id)', 'Duplicate attribute for same device')]

    device_id = fields.Many2one('device.device', required=True)
    device_attribute_id = fields.Many2one('device.attribute', required=True)
    device_attribute_value_id = fields.Many2one('device.attribute.value', required=True)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    device_ids = fields.One2many('device.assignment', 'employee_id', string='Devices Assigned')
