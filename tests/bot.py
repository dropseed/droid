import os

from droid import Droid
from droid.jobs import JobType



class TestJob(JobType):
    pass



bot = Droid(
    name='bot',
    environment=os.environ.get('BOT_ENV', "development"),
    timezone='America/Chicago',
    jobs={
        'config_path': os.path.join(os.path.dirname(__file__), 'jobs'),
        'types': (
            TestJob,
        ),
        'default_job_settings': {
            'github_access_token': "test",
        },
    },
)


if __name__ == '__main__':
    bot.cli()
