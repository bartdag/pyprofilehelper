#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = 0.1

setup(
    name='pyprofilehelper',
    version=version,
    description='Scripts to analyze Python cProfile .prof files.',
    long_description=
    '''
pyprofilehelper is a collection of simple scripts to analyze Python cProfile
.prof files. One script prints the n most time-consuming functions. Another
script prints the time spent in each module.
    ''',
    author='Barthelemy Dagenais',
    author_email='barthelemy@infobart.com',
    license='BSD License',
    url='https://github.com/bartdag/pyprofilehelper',
    packages=[],
    scripts=['cprofread.py', 'cprofscan.py'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities',
    ],
)
