#!/bin/sh

$headers
$slots_statement
cd $working_directory
$command
echo $? > $exit_code_path

