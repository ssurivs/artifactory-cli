from setuptools import setup
setup(
    name = 'artifactory-cli',
    version = '0.0.1',
    packages = ['articli'],
    entry_points = {
        'console_scripts': [
            'articli = articli.__main__:main'
        ]
    })