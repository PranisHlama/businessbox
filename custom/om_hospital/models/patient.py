from odoo import api, fields, models

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread']

    _description = "patient records"
    name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string="Age", tracking=True)
    is_child = fields.Boolean(string="Is Child ?", tracking=True)
    notes = fields.Text(string="Notes", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')], string="Gender", tracking=True)

    capitalized_name = fields.Char(string='Capitalized Name', compute='_compute_capitalized_name', store = True)
    ref = fields.Char(string="Reference", default=lambda self: _('New'))
    @api.model_create_multi
    def create (self, vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('Hospital.patient')
        return super(HospitalPatient, self).create(vals_list)

    @api.depends('name')
    def _compute_capitalized_name(self):
        if self.name:
            self.capitalized_name = self.name.upper()
        else:
            self.capitalized_name = ''

@api.onchange('age')
def _onchange_age(self):
    if self.age <= 10:
        self.is_child = True
    else:
        self.is_child = False
