#!/bin/bash
# generate indices brother

for param_file in $(ls *.parameter)
do
    nohup condor_run "IndriBuildIndex $param_file" &
done
