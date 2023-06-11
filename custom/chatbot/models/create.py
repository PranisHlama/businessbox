from odoo import api, models


# inherit
class MyContacts(models.Model):
    _inherit = 'res.partner'

    # create method
    # @api.model
    # def create(self, vals):
    #     print("Odoo Mates", vals)
    #     vals['website'] =  'TEST.com'
    #     new_contact = super(MyContacts, self).create(vals)
    #     return new_contact
    #
    #
    #     email = new_contact.email
    #
    #     subject = "Welcome to Aakarshan"
    #     body = "Dear {name},\n\nWelcome to our platform. We are excited to have you on board!"
    #
    #     self.env['mail.mail'].create({
    #         'subject': subject,
    #         'email_from': 'pranishlama17@gmail.com',
    #         'email_to': email,
    #         'body_html': body,
    #     }).send()





