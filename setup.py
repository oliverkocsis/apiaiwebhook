from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='apiaiwebhook',

    version='0.1.0.dev1',

    description='API.AI Webhook is a fulfillment microframework for API.AI based on Flask for getting started quickly with API.AI webhooks.',
    long_description=long_description,

    url='https://github.com/paoro-solutions/apiaiwebhook',

    author='Paoro',
    author_email='paoro.biz@outlook.com',

    license='GPLv3',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Topic :: Communications :: Chat',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks'

        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Flask',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],

    keywords='api.ai fullfillment webhook rest restful webservice dispatcher framework flask',

    packages=['apiaiwebhook'],

    install_requires=[
        'Flask>=0.12.1'
    ]
)
