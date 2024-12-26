#!/bin/bash

export W3_FETAP_LOG_CONF=~/w3FeTAp/logging.conf
cd ~/w3FeTAp
source ~/w3FeTAp/pyenv/bin/activate
python -m w3_fetap.w3_fetap_app