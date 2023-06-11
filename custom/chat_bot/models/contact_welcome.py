from odoo import api, models
import openai
openai.api_key = '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'

class Welcome(models.Model):
    _inherit = 'res.partner'


    # OpenAI message
    def create_message(self, name):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Write a welcome letter to a new member at a company",
            max_tokens=100
        )
        message = f"Dear {name},\n\n" + response.choices[0].text.strip()
        return message

    # WhatsApp
    def send_message(self, message, phone_no):
        print(message)
        print(phone_no)
        return True

    def user_info(self, vals):
        print("Info done")
        name = vals.get('name', False)
        email = vals.get('email', False)
        phone = vals.get('phone', False)
        self.create_message(name)
        self.send_message(name, phone, email)

    # Create Method
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            message = self.create_message(vals['name'])
            self.send_message(message, 94857738)
            new_contact = super(Welcome, self).create(vals)
            return new_contact

    # def whatsapp(self, vals_list):
    #     phone = self.create_message(vals['phone'])
    #     self.send_message(phone, vals['phone'])
    #     new_contact = super(Welcome, self).create(vals)
    #     return new_contact


