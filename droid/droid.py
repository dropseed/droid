import logging

from click.testing import CliRunner

from .cli import cli, jobs
from .server import app
from .jobs import JobManager
from .slack import SlackManager
from .email import Email


class Droid:
    def __init__(
        self, jobs, slack={}, email={}, name="droid", timezone=None, environment=None
    ):
        self.name = name
        self.timezone = timezone
        self.environment = environment
        self.configure_logger()

        self.job_manager = JobManager(droid=self, **jobs)

        if slack:
            self.slack_manager = SlackManager(droid=self, **slack)
        else:
            self.slack_manager = None

        if email:
            self.email = Email(droid=self, **email)
        else:
            self.email = None

        app.droid = self
        app.debug = not self.is_production()
        self.server = app

    def __str__(self):
        return self.name

    def cli(self):
        return cli(obj={"droid": self})

    def configure_logger(self):
        self.logger = logging.getLogger(self.name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(asctime)s "%(name)s" %(levelname)s] %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def is_production(self):
        return self.environment == "production"

    def assert_is_production(self):
        assert (
            self.is_production()
        ), "This does not look like your production environment. Be careful."

    def handle_command(self, command_text, environment=None):
        runner = CliRunner()
        result = runner.invoke(
            jobs, command_text.split(), obj={"droid": self, "environment": environment}
        )
        # assert result.exit_code == 0, f'Command failed: {result.exit_code}'

        if result.exception:
            raise result.exception
        return result.output
