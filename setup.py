from setuptools import setup


setup(
    name='arc-cli',
    version='0.1',
    py_modules=['arc_cli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        arc=arc_cli:cli
    ''',
)
