#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest
from aiida_pytest import *

@pytest.fixture(scope='session')
def config(load_config):
    load_config(os.path.abspath('config.yml'))
