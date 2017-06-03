#!/bin/sh
set -e

source_path=$1
source_output=$2
testcase_path=$3

g++ $source_path -o source_bin

cat $testcase_path | ./source_bin > source_output
