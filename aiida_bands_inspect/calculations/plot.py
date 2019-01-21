# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the a calculation class for the ``bands-inspect plot`` command.
"""

from fsc.export import export

from aiida.orm import JobCalculation, DataFactory
from aiida.common.utils import classproperty
from aiida.common.exceptions import InputValidationError
from aiida.common.datastructures import CalcInfo, CodeInfo

from ..io import write_bands


@export
class PlotCalculation(JobCalculation):
    """
    Calculation class for the ``bands_inspect plot`` command.

    Arguments
    ---------
    bands1 : aiida.orm.data.array.bands.BandsData
        First band structure to plot.
    bands2 : aiida.orm.data.array.bands.BandsData
        Second band structure to plot.
    """

    def _init_internal_params(self):
        super(PlotCalculation, self)._init_internal_params()

        self._OUTPUT_FILE_NAME = 'plot.pdf'
        self._default_parser = 'bands_inspect.plot'

    @classproperty
    def _use_methods(cls):
        retdict = super(cls, cls)._use_methods
        retdict['bands1'] = dict(
            valid_types=DataFactory('array.bands'),
            additional_parameter=None,
            linkname='bands1',
            docstring="First bandstructure which is to be plotted"
        )
        retdict['bands2'] = dict(
            valid_types=DataFactory('array.bands'),
            additional_parameter=None,
            linkname='bands2',
            docstring="Second bandstructures which is to be plotted"
        )
        return retdict

    def _prepare_for_submission(self, tempfolder, inputdict):
        ev1_filename = 'eigenvals1.hdf5'
        ev2_filename = 'eigenvals2.hdf5'
        eigenval_file_1 = tempfolder.get_abs_path(ev1_filename)
        write_bands(
            inputdict.pop(self.get_linkname('bands1')), eigenval_file_1
        )
        eigenval_file_2 = tempfolder.get_abs_path(ev2_filename)
        write_bands(
            inputdict.pop(self.get_linkname('bands2')), eigenval_file_2
        )

        try:
            code = inputdict.pop(self.get_linkname('code'))
        except KeyError:
            raise InputValidationError(
                'No code specified for this calculation.'
            )
        if inputdict:
            raise ValidationError(
                'Cannot add other nodes. Remaining input: {}'.
                format(inputdict)
            )

        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = [self._OUTPUT_FILE_NAME]

        codeinfo = CodeInfo()
        codeinfo.cmdline_params = ['plot_bands', ev1_filename, ev2_filename]
        codeinfo.stdout_name = self._OUTPUT_FILE_NAME
        codeinfo.code_uuid = code.uuid
        calcinfo.codes_info = [codeinfo]

        return calcinfo
