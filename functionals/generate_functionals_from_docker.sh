#!/bin/bash
set -e
cd /lax_sod_tube_for_ml/functionals
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages:/usr/local/lib/python3.7/site-packages
python3.7 generate_functionals.py
