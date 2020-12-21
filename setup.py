from setuptools import setup, find_packages
from os.path import join, dirname

import portfOptim

setup(
    name='progOrder',
    version='0.0.1',
    description='Библиотека оптимизации ордеров ',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data=True,
    author_email='eavprog@gmail.com'
)
