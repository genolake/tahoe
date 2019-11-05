
from __future__ import print_function
from setuptools import find_packages, setup
from version import version as tahoe_version

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

import os
import sys

# Utility function to read the README file.
# Used for the long_description.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session='hack')

reqs = [str(ir.req) for ir in install_reqs]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='genolake.tahoe',
    version=tahoe_version,
    description='A scalable genomic visualization tool',
    author='Alyssa Morrow',
    author_email='akmorrow@berkeley.edu',
    url="https://github.com/genolake/tahoe",
    install_requires=reqs,
    dependency_links=[
        'https://test.pypi.org/simple/genolake-adam/'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['*.test.*']))
