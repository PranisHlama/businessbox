from odoo import api, models


class welcome(models.Model):
    _inherit = 'res.partners'

    def createmessage(self, vals):



