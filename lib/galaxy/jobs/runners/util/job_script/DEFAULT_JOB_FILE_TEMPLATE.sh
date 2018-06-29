#!/bin/sh

$headers
$slots_statement
cd $working_directory
#$memory_statement
#$instrument_pre_commands
$command
echo $? > $exit_code_path

