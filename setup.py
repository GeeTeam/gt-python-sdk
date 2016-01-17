#!coding:utf8
from distutils.core import setup

from geetest import VERSION


if __name__ == "__main__":
	setup(
		name="geetest",
		version=VERSION,
        packages=['geetest'],
        url='http://github.com/GeeTeam/gt-python-sdk',
        license='',
        author='Geetest',
        author_email='admin@geetest.com',
        description='Geetest Python SDK',
		)
