import logging

from crontab import CronTab

from .exceptions import InvalidScheduleError, InvalidJobName


class JobType:
    """JobType is to be subclassed to implement a specific type of job"""

    UNKNOWN = "Unknown"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    RUNNING = "Running"

    def __init__(
        self, name, droid, schedule=None, can_be_run_manually=False, *args, **kwargs
    ):
        self.state = self.UNKNOWN
        self.results = None

        self.name = name
        if " " in self.name:
            raise InvalidJobName(self.name)

        self.droid = droid
        self.schedule = schedule
        self.can_be_run_manually = can_be_run_manually

        # TODO run_by_schedule -- a way to change behavior based on manual/scheduled run

        if self.schedule:
            # TODO make a JobSchedule class?
            # prepend the minute 0 automatically
            if len(self.schedule.split()) != 4:
                raise InvalidScheduleError(
                    self.schedule,
                    "Schedule should have 4 parts: HOURS DAY_OF_MONTH MONTH DAY_OF_WEEK",
                )

            self.crontab = CronTab("0 " + self.schedule)
        else:
            self.crontab = None

        self._configure_logger()

    def __str__(self):
        return f"{self.name} ({self.__class__})"

    def _configure_logger(self):
        self.logger = logging.getLogger(self.name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(asctime)s "%(name)s" %(levelname)s] %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def scheduled_to_run(self, when):
        if not self.crontab:
            return False

        # currently we don't care about anything beyond the hour
        when = when.replace(minute=0, second=1, microsecond=0)
        seconds_since_last_run = self.crontab.previous(when)
        # if should have run in this hour, then 'last run' will be 1 sec ago
        return seconds_since_last_run == -1.0

    def run(self):
        raise NotImplementedError

    def notify_for_state(self):
        if self.state == self.SUCCEEDED:
            self.logger.debug("Triggering on_success")
            self.on_success()
        elif self.state == self.FAILED:
            self.logger.debug("Triggering on_failure")
            self.on_failure()
        else:
            raise Exception(f'Unsure how to notify about state "{self.state}"')

    def succeeded(self):
        self.state = self.SUCCEEDED

    def failed(self):
        self.state = self.FAILED

    def on_success(self):
        """Custom code to run on success"""
        pass

    def on_failure(self):
        """Custom code to run on failure"""
        pass

    def on_error(self, exception=None):
        """Custom code to run on error"""
        pass
