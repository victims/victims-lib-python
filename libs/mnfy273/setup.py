from distutils.core import setup
import sys

with open('docs/index.rst') as file:
    long_description = file.read().partition('.. END README')[0]

version = '27.3.0'
assert version.startswith('{}{}'.format(*sys.version_info))

setup(
    name='mnfy27',
    # First digit is the Massive/feature version of Python, rest are
    # feature/bugfix for mnfy.
    version='27.3.0',
    author='Dulitha Ranatunga,Brett Cannon',
    author_email='dulitharanatunga@gmail.com',
    url='www.dulitharanatunga.com',
    py_modules=['mnfy'],  # Don't install test code since not in a package
    license='Apache Licence 2.0',
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
    ],
)
