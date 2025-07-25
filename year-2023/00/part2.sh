#!/usr/bin/env bash

if [ $# -eq 0 ]; then
    echo "Please provide an input file."
    exit 1
fi

# solution

input=()

while IFS= read -r line; do
    input+=("$line")
done < "$1"

echo "${input[@]}"