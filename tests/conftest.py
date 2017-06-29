#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest
from aiida_pytest import *

@pytest.fixture(scope='session')
def config(configure_from_file):
    configure_from_file(os.path.abspath('config.yml'))
