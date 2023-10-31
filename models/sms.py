from odoo import api, fields, models, http
import africastalking
import json
import requests

from odoo.odoo.http import Response


class AfricasSms(models.Model):
    _name = "africas.sms"
    _description = "Send sms"

    name = fields.Char(string="Name", required=True)
    recipients = fields.Char(string="Recipients", required=True)
    message = fields.Text(string="Message", required=True)
    sender = fields.Char(string="SenderId", required=True)

    def send_sms(self):
        API_KEY = '20bb6937d1eaed5026757e0ae65b6aa84b28f0fcb79a0a01f73216d56cf43c1e'
        BASE_URL = 'https://api.africastalking.com/version1/messaging'
        username = 'aft_sms'

        headers = {"apiKey": API_KEY,
                   "Content-Type": "application/x-www-form-urlencoded",
                   "Accept": "application/json"
                   }
        recipients = self.recipients
        message = self.message
        sender = self.sender

        callback_url = 'http://localhost:8069/Delivery-reports'
        '''callback_url = 'http://localhost:8069/Incoming-messages'
        '''

        data = {
            "username": username,
            "to": recipients,
            "message": message,
            # "from": sender,
            "bulkSMSMode": 1,  # Set to 1 for bulk SMS mode
            "enqueue": 1,  # Set to 1 to enable delivery reports
            "callback": callback_url,

        }
        response = requests.post(BASE_URL, headers=headers, data=data)
        if response.status_code == 200:
            response_data = response.json()
            self.write({
                "response_data": response_data,
            })
        elif response.status_code == 201:
            print("Resource Created", response.text)
        else:
            print("Error:", response.status_code, response.text)

    @http.route("/Delivery-reports", type='json', auth="none", methods=['POST'], csrf=False)
    def delivery_reports(self, **data):
        print("Delivery Reports data:", data)
        return Response(status=200)

    @http.route("/Incoming-messages", type='json', auth="none", methods=['POST'], csrf=False)
    def incoming_messages(self, **data):
        print("Incoming Message Data", data)
        return Response(status=200)
