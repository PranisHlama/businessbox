from odoo import api, models
import openai

openai.api_key = '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'


class Welcome(models.Model):
    _inherit = 'res.partner'

    def create_message(self, name):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Write a welcome letter to a new {name} at a company",
            max_tokens=100
        )
        message = response.choices[0].text.strip()
        return message

    # Create Method
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            message = self.create_message(vals['name'])
            self.send_message(message, 94857738)
            new_contact = super(Welcome, self).create(vals)
            return new_contact

    # OpenAI message

    def send_message(self,message, phone_no):
        print(message)
        print(phone_no)
        return True

    def user_info(self, vals):
        print("Info done")
        name = vals.get('name', False)
        email = vals.get('email', False)
        phone = vals.get('phone', False)
        create_message()
        send_message(name, phone, email)

    # WhatsApp
    # def whatsapp(self, vals_list):
    #     phone = create_message(vals['phone'])
    #     self.send_message(phone, vals['phone'])
    #     new_contact = super(Welcome, self).create(vals)
    #     return new_contact
