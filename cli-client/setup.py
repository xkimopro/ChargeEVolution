from setuptools import setup
setup(
    name='cli',
    version='0.0.1',
    install_requires = [
        'Click',
    ],
    entry_points ='''
        [console_scripts]
        ev_group54=cli:cli
    ''',
)