from odoo import api, models


class Welcome(models.Model):
    _inherit = 'res.partner'

    # Create Method
    @api.model
    def create(self, vals):
        print("Odoo Mates", vals)
        vals['website'] = 'TEST.com'
        new_contact = super(Welcome, self).create(vals)
        return new_contact

    # OpenAI message
    def create_message(name):
        print('create message')
        message = f"Dear {name},\n\nWelcome to our platform. We are excited to have you on board"
        return message

    # WhatsApp
    def send_message(name, phone_no, email):
        print('send message')
        print(name)
        print(phone_no)
        print(email)

    def user_info(self,vals):
        print("Info done")
        name = vals.get('name', False)
        email = vals.get('email', False)
        phone = vals.get('phone', False)
        self.create_message(name)
        self.send_message(name, phone, email)
