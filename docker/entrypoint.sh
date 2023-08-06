#!/bin/zsh

pdm install

eval "$(pdm --pep582)"
export PATH=$PATH:${MY_PYTHON_PACKAGES}/bin

tail -f /dev/null
