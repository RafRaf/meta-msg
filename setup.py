from setuptools import setup, find_packages


description = \
    "Meta-msg it's an additional layer for your binary exchange " \
    "systems. It lets you add status/error codes to your messages and " \
    "raise/handle errors between microservices in traditional (pythonic) way."

setup(
    name='meta-msg',
    version='0.1',
    packages=find_packages(exclude=('tests/*',)),
    author='RafRaf',
    author_email='smartrafraf@gmail.com',
    description=description,
    long_description=description,
    license='MIT',
    keywords=['message', 'nats', 'rabbitmq'],
    test_suite='tests',
    url='https://github.com/RafRaf/meta-msg/',
)
