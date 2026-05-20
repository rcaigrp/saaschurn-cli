from setuptools import setup

setup(
    name='SaaSChurn-CLI',
    version='0.1.0',
    packages=['saaschurn'],
    install_requires=[
        'stripe',
        'slack_sdk',
        'rich',
        'click',
    ],
)
