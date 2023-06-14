from odoo import api, models
import openai

from twilio.rest import Client

# whatsapp_API_KEY = "App 2f66efa403936a35a76e8d7c8b5bd17e-b6b1cd33-51bc-4ec7-a004-ee98a0176b5a"
whatsapp_API_KEY = 'adf22c93f9c7265950ce5e850ab4174d'
# headers = {
#     'Authorization': whatsapp_API_KEY,
#     'Content-Type': 'application/json',
#     'Accept': 'application/json'
# }

openai.api_key = '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'


class Welcome(models.Model):
    _inherit = 'res.partner'

    def create_message(self, vals):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Write a welcome letter to {employee_name} at a company named Aakarshan ",
            max_tokens=100

        )
        # name = vals['name']
        message = response.choices[0].text.strip()
        return message


    # Create Method
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            message = self.create_message(vals['name'])
            self.send_message(message, 9840724609)
            new_contact = super(Welcome, self).create(vals)
            return new_contact

    # OpenAI message
    def send_message(self, message, phone_no):
        print(message)
        print(phone_no)
        return True


    def user_info(self, vals):
        print("Info done")
        name = vals.get('name', False)
        email = vals.get('email', False)
        phone = vals.get('phone', False)
        self.create_message()
        self.send_message(name, phone, email)





