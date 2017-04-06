#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from aiida.orm import DataFactory
from aiida.parsers.parser import Parser
from aiida.tools.codespecific.bandstructure_utils.io import read_bands

class ModelParser(Parser):
    """
    Parse TBmodels output to a SinglefileData containing the model file.
    """
    def parse_with_retrieved(self, retrieved):
        try:
            out_folder = retrieved[self._calc._get_linkname_retrieved()]
        except KeyError:
            self.logger.error("No retrieved folder found")

        bands_file = out_folder.get_abs_path(self._calc._OUTPUT_FILE_NAME)
        new_nodes_list = [('bands', read_bands(bands_file))]

        return True, new_nodes_list
