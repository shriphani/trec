#!/bin/bash

for xml_file in $(cat xml_files);
do
	nohup condor_run "python snippets_trec_format.py $xml_file" &
done