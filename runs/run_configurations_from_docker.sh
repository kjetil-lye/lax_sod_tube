#!/bin/bash
set -e
cd /lax_sod_tube_for_ml/runs
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages:/usr/local/lib/python3.7/site-packages
cp /usr/lib/libsobol.so ./
python3.7 run_configurations.py "$@"
