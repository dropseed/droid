import logging
import datetime

from crontab import CronTab


class Job:
    UNKNOWN = 'Unknown'
    SUCCEEDED = 'Succeeded'
    FAILED = 'Failed'
    RUNNING = 'Running'

    def __init__(self, name, droid, schedule=None, can_be_run_manually=False, *args, **kwargs):
        self.state = self.UNKNOWN
        self.results = None

        self.name = name
        self.droid = droid
        self.schedule = schedule
        self.can_be_run_manually = can_be_run_manually

        # so you can send it to a specific response url (other other webhook than default)
        self.slack_webhook_url = kwargs.get('slack_webhook_url', None)

        if self.schedule:
            self.crontab = CronTab(self.schedule)
        else:
            self.crontab = None

        self.configure_logger()

    def __str__(self):
        return f'{self.name} ({self.__class__})'

    def configure_logger(self):
        self.logger = logging.getLogger(self.name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s "%(name)s" %(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def scheduled_to_run_in_this_hour(self, from_when=None):
        # get the these first, so microseconds are in order
        seconds_until_next_run = self.crontab.next(from_when)
        seconds_since_last_run = self.crontab.previous(from_when)
        now = datetime.datetime.now()

        seconds_passed_this_hour = (now.minute * 60) + now.second + (now.microsecond / 1000000)
        seconds_remaining_this_hour = 3600 - seconds_passed_this_hour

        will_run = seconds_until_next_run < seconds_remaining_this_hour
        would_have_run = (seconds_since_last_run * -1) < seconds_passed_this_hour

        return will_run or would_have_run

    def run(self):
        raise NotImplementedError

    def notify_for_state(self):
        if self.state == self.SUCCEEDED:
            self.logger.debug('Triggering on_success')
            self.on_success()
        elif self.state == self.FAILED:
            self.logger.debug('Triggering on_failure')
            self.on_failure()
        else:
            raise Exception(f'Unsure how to notify about state "{self.state}"')

    def on_success(self):
        """Custom code to run on success"""
        pass

    def on_failure(self):
        """Custom code to run on failure"""
        pass

    def on_error(self, exception=None):
        """Custom code to run on error"""
        pass

    def send_slack_message(self, json):
        self.droid.slack_manager.send(json, url=self.slack_webhook_url)
