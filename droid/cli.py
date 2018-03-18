import click


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.pass_context
def test(ctx):
    droid = ctx.obj['droid']
    click.secho(f'{droid} loaded successfully!', fg='green')


@cli.command()
@click.pass_context
def server(ctx):
    droid = ctx.obj['droid']
    droid.server.run()


@cli.group()
@click.pass_context
def jobs(ctx):
    pass


@jobs.command('list')
@click.option('--scheduled', is_flag=True, default=False)
@click.pass_context
def jobs_list(ctx, scheduled):
    droid = ctx.obj['droid']

    if scheduled:
        jobs = droid.job_manager.get_scheduled_jobs()
    else:
        jobs = droid.job_manager.jobs

    click.secho(f'There are {len(jobs)} jobs')
    for j in jobs:
        click.secho(f'- {j}')


@jobs.command('run')
@click.argument('job_name')
@click.option('--notifications/--no-notifications', default=True)
@click.pass_context
def jobs_run(ctx, job_name, notifications):
    droid = ctx.obj['droid']
    droid.job_manager.run_job_by_name(job_name, send_notifications=notifications)


@jobs.command('scheduled')
@click.option('--notifications/--no-notifications', default=True)
@click.pass_context
def jobs_scheduled(ctx, notifications):
    droid = ctx.obj['droid']
    droid.job_manager.run_scheduled_jobs(send_notifications=notifications)
