# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import re
from setuptools import setup, find_packages

# Get the version number
with open('./aiida_bands_inspect/__init__.py') as f:
    match_expr = "__version__[^'\"]+(['\"])([^'\"]+)"
    version = re.search(match_expr, f.read()).group(2).strip()

if __name__ == '__main__':
    setup(
        name='aiida-bands-inspect',
        version=version,
        description='AiiDA Plugin for running bands_inspect',
        author='Dominik Gresch',
        author_email='greschd@gmx.ch',
        url='https://aiida-bands-inspect.readthedocs.io',
        license='Apache 2.0',
        classifiers=[
            'Development Status :: 3 - Alpha', 'Environment :: Plugins',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.6',
            'Topic :: Scientific/Engineering :: Physics'
        ],
        keywords='bandstructure aiida workflows',
        packages=find_packages(exclude=['aiida']),
        include_package_data=True,
        setup_requires=['reentry'],
        reentry_register=True,
        install_requires=[
            'h5py',
            'aiida-core>=1.0.0a4',
            'fsc.export',
        ],
        extras_require={
            'dev': [
                'numpy',
                'aiida-pytest',
                'pytest',
                'yapf==0.25',
                'pre-commit',
            ]
        },
        entry_points={
            'aiida.calculations': [
                'bands_inspect.difference = aiida_bands_inspect.calculations.difference:DifferenceCalculation',
                'bands_inspect.plot = aiida_bands_inspect.calculations.plot:PlotCalculation'
            ],
            'aiida.parsers': [
                'bands_inspect.bands = aiida_bands_inspect.parsers.bands:BandsParser',
                'bands_inspect.difference = aiida_bands_inspect.parsers.difference:DifferenceParser',
                'bands_inspect.plot = aiida_bands_inspect.parsers.plot:PlotParser'
            ],
        },
    )
