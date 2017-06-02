#!/bin/sh
set -e

source_path=$1
source_output=$2
solution_path=$3
solution_output=$4
testcase_path=$5

g++ $source_path -o source_bin
g++ $solution_path -o solution_bin

cat $testcase_path | ./source_bin > source_output
cat $testcase_path | ./solution_bin > solution_output
