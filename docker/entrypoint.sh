#!/bin/zsh

pdm install

eval "$(pdm --pep582)"

tail -f /dev/null
