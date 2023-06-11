from odoo import api, models


# inherit
class MyContacts(models.Model):
    _inherit = 'res.partner'

    # create method
    @api.model
    def create(self, vals):
        print("Odoo Mates", vals)
        vals['website'] = 'TEST.com'
        new_contact = super(MyContacts, self).create(vals)
        return new_contact


