#!/bin/bash

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

# Be verbose, and stop with error as soon there's one
set -ev

case "$TEST_TYPE" in
    tests)
        # Run the AiiDA tests
        python ${TRAVIS_BUILD_DIR}/.travis-data/configure.py ${TRAVIS_BUILD_DIR}/.travis-data ${TRAVIS_BUILD_DIR}/tests;
        cd ${TRAVIS_BUILD_DIR}/tests; py.test --quiet-wipe --print-status
        ;;
    pre-commit)
        pre-commit run --all-files
        ;;
esac
