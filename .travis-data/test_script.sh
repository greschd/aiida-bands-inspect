#!/bin/bash

# Be verbose, and stop with error as soon there's one
set -ev

case "$TEST_TYPE" in
    tests)
        # Run the AiiDA tests
        cp ${TRAVIS_BUILD_DIR}/.travis-data/test_config.yml ${TRAVIS_BUILD_DIR}/tests/;
        # python ${TRAVIS_BUILD_DIR}/.travis-data/configure.py ${TRAVIS_BUILD_DIR}/.travis-data ${TRAVIS_BUILD_DIR}/tests;
        export AIIDA_PATH="${TRAVIS_BUILD_DIR}/tests"
        cd ${TRAVIS_BUILD_DIR}/tests; py.test --quiet-wipe
        ;;
    pre-commit)
        pre-commit run --all-files || git status --short && git diff
        ;;
esac