from setuptools import setup

setup(
    name='autoguiwinio',
    version='0.0.1',
    author='guo.jiaqiang',
    author_email='guojq0ing@outlook.com',
    description=u'Simulating the input based on i8042, useful for DirectInput/Windows events are blocked',
    packages=['autoguiwinio'],
    install_requires=["ctypes"],
)