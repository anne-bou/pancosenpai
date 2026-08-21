# ============================================================
# PancoSenpai Project — https://github.com/anne-bou/pancosenpai
# Copyright (C) 2026 Anne Bouillard
# License: BSD-3-Clause
#
# This file is part of the PancoSenpai project.
# Redistribution must retain this copyright notice and license.
# ============================================================

__author__ = "Anne Bouillard"
__email__ = "anne.bouillard@ens.fr"
__license__ = "BSD-3-Clause"

"""The setup script."""

from setuptools import setup

README = ""
try:
    with open('README.rst') as readme_file:
        README = readme_file.read()
except:
    pass

HISTORY = ""
try:
    with open('HISTORY.rst') as history_file:
        history = history_file.read()
except:
    pass

requirements = ['panco', 'customtkinter']

setup(
    author="Anne Bouillard",
    author_email='anne.bouillard@ens.com',
    description="Small Graphical Toolbox for getting used with Panco",
    install_requires=requirements,
    include_package_data=True,
    # install_requires=requirements,
    license="BSD-3",
    long_description=README + '\n\n' + HISTORY,
    keywords='pancoSenpai',
    name='pancoSenpai',
    packages=['pancoSenpai', 'pancoSenpai.View', 'pancoSenpai.Controller', 'pancoSenpai.Utils'],
    py_modules=["main"],
    url='https://github.com/anne-bou/pancosenpai',
    version='0.1.0',
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "pancoSenpai = pancoSenpai.main:main"
        ]}
)