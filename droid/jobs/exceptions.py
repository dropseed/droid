class JobTypeDoesNotExist(Exception):
    def __init__(self, job_type):
        self.job_type = job_type


class InvalidScheduleError(Exception):
    def __init__(self, schedule, message):
        self.schedule = schedule
        self.message = message


class JobNotFound(Exception):
    def __init__(self, job_name):
        self.job_name = job_name


class InvalidJobName(Exception):
    def __init__(self, job_name):
        self.job_name = job_name
