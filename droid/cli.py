import click

from droid.jobs.exceptions import JobNotFound


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
    assert not ctx.obj.get('environment', None), 'Can only run this from the command line'
    droid.server.run()


@cli.group()
@click.pass_context
def jobs(ctx):
    pass


@jobs.command('list')
@click.option('--scheduled', is_flag=True, default=False)
@click.option('--when')
@click.pass_context
def jobs_list(ctx, scheduled, when):
    droid = ctx.obj['droid']

    if scheduled:
        jobs = droid.job_manager.get_scheduled_jobs(when)
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
    try:
        droid.job_manager.run_job_by_name(job_name, send_notifications=notifications)
    except JobNotFound as e:
        environment = ctx.obj.get('environment', None)
        if environment == 'slack':
            click.echo(f'"{e.job_name}" was not found. These are the available jobs:')
            ctx.invoke(jobs_list)
        else:
            raise e


@jobs.command('scheduled')
@click.option('--notifications/--no-notifications', default=True)
@click.option('--when')
@click.pass_context
def jobs_scheduled(ctx, notifications, when):
    droid = ctx.obj['droid']
    assert not ctx.obj.get('environment', None), 'Can only run this from the command line'
    droid.job_manager.run_scheduled_jobs(send_notifications=notifications, when=when)
