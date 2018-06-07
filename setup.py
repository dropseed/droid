# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


# with open('README.rst') as f:
#     readme = f.read()
#

setup(
    name='droid',
    version='0.1.1',
    description='',
    # long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/dropseed/droid',
    author='Dropseed, LLC',
    author_email='python@dropseed.io',
    python_requires='>=3.6.0',
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
        'slackclient',
    ),
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
