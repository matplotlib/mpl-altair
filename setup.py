from __future__ import print_function
import os
from setuptools import setup


try:
    descr = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
except IOError:
    descr = ''

try:
    from pypandoc import convert
    descr = convert(descr, 'rst', format='md')
except ImportError:
    pass

classifiers = [
    'Development Status :: 2 - Pre-Alpha'
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: Python Software Foundation License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Scientific/Engineering :: Visualization',
    classifiers=classifiers,
    ]


setup_parameters = dict(
    name="mpl-altair",
    version='0.0.0',
    description="Convert altair objects to Matplotlib Figures",
    author="Matplotlib Development Team",
    install_requires=['matplotlib>=2.2.0', 'altair>=2'],
    author_email="matplotlib-users@python.org",
    url="https://github.com/matplotlib/mpl-altair",
    packages=['mplaltair'],
    python_requires='>=3.5',
    license="BSD",
    platforms='any',
    long_description=descr)

setup(**setup_parameters)
