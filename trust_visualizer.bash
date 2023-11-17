#!/bin/bash

##############################################################################
# Author: @Sma-Das
#
# Description: Simplify usage of Docker to execute this script.
#           
#
# License: BSD 3-clause
##############################################################################

# Check if the number of arguments is correct
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file_path>"
    exit 1
fi

file_path=$1

# Check if the file path exists
if [ ! -e "$file_path" ]; then
    echo "Error: File path '$file_path' does not exist."
    exit 1
fi

# Check if the file path is a regular file
if [ ! -f "$file_path" ]; then
    echo "Error: '$file_path' is not a regular file."
    exit 1
fi

filename=$(basename "$file_path")

docker run --rm -v "${file_path}":"/${filename}" smadas/py2trust python "/${filename}"

exit 0
