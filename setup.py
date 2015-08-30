import os
from setuptools import setup, find_packages 


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-jet',
    version=__import__('jet').VERSION,
    description='Modern template for Django admin interface with improved functionality',
    long_description=read('README.rst'),
    author='Denis Kildishev',
    author_email='support@jet.geex-arts.com',
    url='https://github.com/geex-arts/django-jet',
    packages=find_packages(),
    license='Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'License :: Free for non-commercial use',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Environment :: Web Environment',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ],
    zip_safe=False,
    include_package_data=True
)
