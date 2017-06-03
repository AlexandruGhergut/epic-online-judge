#!/bin/sh
set -e

source_path=$1
source_output=$2
testcase_path=$3

cat $testcase_path | python $source_path > source_output
