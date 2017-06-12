# -*- coding: utf-8 -*-
"""
setup: usage: pip install -e .[graphs]
"""

from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='aiida-bandstructure-utils',
        version='0.0.0a1',
        description='AiiDA Plugin for running bandstructure_utils',
        author='Dominik Gresch',
        author_email='greschd@gmx.ch',
        license='GPL',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Plugins',
            'Framework :: AiiDA',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering :: Physics'
        ],
        keywords='bandstructure aiida workflows',
        packages=find_packages(exclude=['aiida']),
        include_package_data=True,
        setup_requires=[
            'reentry'
        ],
        reentry_register=True,
        install_requires=[
            'h5py',
            'aiida-core',
        ],
        extras_require={
        },
        entry_points={
            'aiida.calculations': [
                'bandstructure_utils.difference = aiida_bandstructure_utils.calculations.difference:DifferenceCalculation',
            ],
            'aiida.parsers': [
                'bandstructure_utils.bands = aiida_bandstructure_utils.parsers.bands:BandsParser',
                'bandstructure_utils.difference = aiida_bandstructure_utils.parsers.difference:DifferenceParser',
            ],
        },
    )
