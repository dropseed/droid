import requests


class SlackManager:
    def __init__(self,
                 droid,
                 webhook_url,
                 verification_token,
                 command_request_handler,
                 action_request_handler,
                 options_request_handler
                 ):
        self.droid = droid
        self.webhook_url = webhook_url
        self.verification_token = verification_token
        self.command_request_handler = command_request_handler
        self.action_request_handler = action_request_handler
        self.options_request_handler = options_request_handler

    def request_is_valid(self, request):
        token = request.form['token']
        return self.verification_token == token

    def send(self, json, url=None):
        response = requests.post(url or self.webhook_url, json=json)
        self.droid.logger.debug(response)
        response.raise_for_status()
