from slack import WebClient


class SlackManager:
    def __init__(self,
                 droid,
                 bot_token,
                 verification_token,
                 command_request_handler=None,
                 action_request_handler=None,
                 options_request_handler=None
                 ):
        self.droid = droid
        self.bot_token = bot_token
        self.verification_token = verification_token
        self.command_request_handler = command_request_handler
        self.action_request_handler = action_request_handler
        self.options_request_handler = options_request_handler

        self.client = WebClient(token=self.bot_token)

    def request_is_valid(self, request):
        token = request.form['token']
        return self.verification_token == token

    def send(self, json):
        response = self.client.chat_postMessage(**json)

        self.droid.logger.debug(response)

        if not response['ok']:
            raise Exception(f'Slack API call failed: {response}')
