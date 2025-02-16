from twilio.rest import Client


class TwilioClient:

    def __init__(self, config: dict):
        self.sid = config["sid"]
        self.auth_token = config["auth_token"]
        self.sender_phone_number = config["sender_phone_number"]
        self.client = Client(username=self.sid, password=self.auth_token)

    def send_sms(self, message_body: str, receiver: str):
        try:
            self.client.messages.create(
                body=message_body,
                from_=self.sender_phone_number,
                to=receiver,
            )
            print("TwilioClient: SMS successfully sent!")
        except Exception as exception:
            print("TwilioClient: An exception has occurred:", exception)
