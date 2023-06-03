from odoo import api, fields, models


class hospitalpatient(models.Model):
    _name= "hospital.patient"
    _description= "Hospital patient records"

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(sting="Age")
    is_child = fields.Boolean(string="is child?")
    notes = fields.Text(string="Some description")
    gender = fields.Selection([('male','Male'), ('female','Female'), ('others','Others')],string="Gender")
