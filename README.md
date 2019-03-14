<p align="center"><img src="icon.svg" alt="Droid" height="140px"></p>
<h1 align="center">Droid</h1>

*In development.*

Droid is a framework for building a bot in Python.

There's nothing necessarily new or unique here -- just our way of doing it. What
we wanted was:

- a language we like, know, and use often (Python)
- should not require a background task queue/workers (i.e. celery)
- should not require a database
- should be easy to deploy (see previous points)
- eases integration with Slack
- should be easy to have it do things on a schedule (crontab-like)
- should be easy to teach it how to do new things (minimal amount of new code)

In particular, the primary responsibility of our bots is to act as a sentinel,
of sorts. Keeping an eye on the systems and tools that we use, and letting us
know when things look out of place or some action needs to be taken to clean
things up.

## Jobs

Jobs are what a droid does.

You define your jobs in YAML, making it easier on the eyes and less
intimidating for non-technical users.

```yml
jobs:
- type: CheckOvertime
  name: check_overtime_for_dave
  schedule: "17 * * Fri"  # 5pm on Fridays
  can_be_run_manually: true
  settings:
    employee_name: Dave

- type: CheckOvertime
  name: check_overtime_for_joel
  schedule: "17 * * Fri"  # 5pm on Fridays
  can_be_run_manually: true
  settings:
    employee_name: Joel
```

Then the code that runs your job is written in Python.

```python
class CheckOvertime(JobType):
    def __init__(self, employee_name, *args, **kwargs):
        # save any settings you need to run a job
        self.employee_name = employee_name
        super().__init__(*args, **kwargs)

    def run(self):
        self.employee_hours = get_hour_for_employee_this_week(self.employee_name)
        if self.employee_hours > 40:
            self.failed()
        else:
            self.succeeded()

    def on_failure(self):
        self.send_slack_message({'text': f'{self.employee_name} has {self.employee_hours} this week!'})
```

Jobs can be run either on a schedule, or on-demand via Slack or the command
line. Scheduled jobs are good for having your droid check on things
periodically, and letting you know of the results.
