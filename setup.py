# Copyright (c) 2020 All Rights Reserved
# Author: William H. Guss, Brandon Houghton

import os
import sys
import json
from os.path import isdir

import subprocess
import pathlib
import setuptools
from setuptools import Command
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.install_lib import install_lib
from distutils.command.build import build

from setuptools.dist import Distribution
import shutil

with open("README.md", "r", encoding="utf-8") as fh:
    markdown = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

MALMO_BRANCH = "minerl"
MALMO_VERSION = "0.37.0"
MALMO_DIR = os.path.join(os.path.dirname(__file__), 'minerl', 'Malmo')
BINARIES_IGNORE = shutil.ignore_patterns(
    'build',
    'bin',
    'dists',
    'caches',
    'native',
    '.git',
    'doc',
    '*.lock',
    '.gradle',
    '.minecraftserver',
    '.minecraft')
# TODO: THIS IS NOT ACTUALLY IGNORING THE GRADLE.

# TODO: Potentially add locks to the binary ignores.


try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


    # @minecraft_build
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False

except ImportError:
    bdist_wheel = None


# https://github.com/chinmayshah99/PyDP/commit/2ddbf849a749adad5d5db10d4d7e3479567087f3
# Bug here https://github.com/python/cpython/blob/28ab3ce92402d86aa400960d38f0d69f498bb677/Lib/distutils/command/install.py#L335
# Original fix proposed here: https://github.com/google/or-tools/issues/616
class BinaryDistribution(Distribution):
    """This class is needed in order to create OS specific wheels."""

    def has_ext_modules(self):
        return True


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

class InstallPlatlib(install):
    def finalize_options(self):
        install.finalize_options(self)
        # Hmm so this is  wierd. When is has_ext_modules tru?
        if self.distribution.has_ext_modules():
            self.install_lib = self.install_platlib


class InstallWithMinecraftLib(install_lib):
    """Overrides the build command in install lib to build the minecraft library
    and place it in the build directory.
    """

    def build(self):
        super().build()

class CustomBuild(build):
    def run(self):
        super().run()


class ShadowInplace(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        pass

# Don't build binaries (requires Java) on readthedocs.io server.
if os.environ.get("READTHEDOCS"):
    print("READTHEDOCS env var is set; performing partial package install only.")
    cmdclass = {}
else:
    cmdclass = {
        'bdist_wheel': bdist_wheel,
        'install': InstallPlatlib,
        'install_lib': InstallWithMinecraftLib,
        'build_malmo': CustomBuild,
        'shadow_develop': ShadowInplace,
    }

setuptools.setup(
    name='minerl',
    version=os.environ.get('MINERL_BUILD_VERSION', '1.0.2'),
    description='MineRL environment and data loader for reinforcement learning from human demonstration in Minecraft',
    long_description=markdown,
    long_description_content_type="text/markdown",
    url='http://github.com/minerllabs/minerl',
    author='MineRL Labs',
    author_email='minerl@andrew.cmu.edu',
    license='MIT',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    distclass=BinaryDistribution,
    include_package_data=True,
    cmdclass=cmdclass,
)
