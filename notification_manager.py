from multiprocessing.connection import Client


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self, twilio_account_sid=None, twilio_auth_token=None):
        self.client = Client(twilio_account_sid, twilio_auth_token)

    def send_sms(self, message, twilio_virtual_number=None, twilio_verified_number=None):
        message = self.client.messages.create(
            body=message,
            from_=twilio_virtual_number,
            to=twilio_verified_number
        )
        # Prints if successfully sent.
        print(message.sid)
