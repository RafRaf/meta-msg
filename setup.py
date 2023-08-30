from setuptools import setup, find_packages


setup(
    name='meta-msg',
    version='0.1',
    packages=find_packages(exclude=('tests/*',)),
    author='RafRaf',
    author_email='smartrafraf@gmail.com',
    license='MIT',
    keywords=['message', 'nats', 'rabbitmq'],
    test_suite='tests',
)
