#!coding:utf8
import sys

try:
    from setuptools import setup
except:
    from distutils.core import setup
VERSION = "3.2.0"


if __name__ == "__main__":
    with open('requirements.txt') as f:
        required = f.read().splitlines()
    setup(
        name="geetest",
        version=VERSION,
        packages=['geetest'],
        url='http://github.com/GeeTeam/gt-python-sdk',
        license='',
        author='Geetest',
        author_email='admin@geetest.com',
        description='Geetest Python SDK',
        install_requires=required,
    	)
