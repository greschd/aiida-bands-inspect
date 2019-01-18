#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from __future__ import division, print_function, unicode_literals

from aiida.orm import DataFactory, CalculationFactory


def run():
    code = Code.get_from_string('bands_inspect')
    calc = CalculationFactory('bands_inspect.difference')()
    calc.use_code(code)

    BandsData = DataFactory('array.bands')
    bands1 = BandsData()
    bands2 = BandsData()
    kpoints = [[0.1, 0.2, 0.3], [0., 0.5, 0.5]]
    bands1.set_kpoints(kpoints)
    bands2.set_kpoints(kpoints)
    bands1.set_bands([[1, 2, 3], [1, 2, 3]])
    bands2.set_bands([[2, 2, 3], [1, 2, 2]])
    calc.use_bands1(bands1)
    # from aiida.orm.data.base import Int
    calc.use_bands2(bands2)

    calc.set_resources(dict(num_machines=1, tot_num_mpiprocs=1))
    calc.set_withmpi(False)
    calc.set_computer(Computer.get('localhost'))
    calc.store_all()
    calc.submit()
    print('Submitted calculation', calc.pk)


if __name__ == '__main__':
    run()
