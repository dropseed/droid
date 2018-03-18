# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


# with open('README.rst') as f:
#     readme = f.read()
#
# with open('LICENSE') as f:
#     license = f.read()

setup(
    name='droid',
    version='0.1.0',
    description='',
    # long_description=readme,
    author='Dropseed, LLC',
    author_email='python@dropseed.io',
    install_requires=(
        'configyaml==0.4.0',
        'click',
        'requests',
        'humanize',
        'crontab',
        'raven[flask]',
        'Flask',
        'gunicorn',
        'maya',
        'flask-dance',
        'redis',
        'traitlets',
    ),
    url='https://github.com/dropseed/droid',
    # license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
