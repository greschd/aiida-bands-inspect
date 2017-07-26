# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='aiida-bands-inspect',
        version='0.0.0a1',
        description='AiiDA Plugin for running bands_inspect',
        author='Dominik Gresch',
        author_email='greschd@gmx.ch',
        license='GPL',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Plugins',
            'Framework :: AiiDA',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
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
        extras_require={'test': ['numpy', 'aiida-pytest', 'pytest']},
        entry_points={
            'aiida.calculations': [
                'bands_inspect.difference = aiida_bands_inspect.calculations.difference:DifferenceCalculation',
            ],
            'aiida.parsers': [
                'bands_inspect.bands = aiida_bands_inspect.parsers.bands:BandsParser',
                'bands_inspect.difference = aiida_bands_inspect.parsers.difference:DifferenceParser',
            ],
        },
    )
