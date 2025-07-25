#!/usr/bin/env bash

if [ $# -eq 0 ]; then
    echo "Please provide an input file."
    exit 1
fi

# solution

sum=0

while IFS= read -r line; do
    # ignore EOF line
    [ -z "$line" ] && continue

    # get every digit from a string
    digits=()

    for ((i=0; i<${#line}; i++)); do
        c=${line:$i:1}
        if [[ $c =~ ^[0-9]$ ]]; then
            digits+=("$c")
        fi
    done

    # keep the first and last digit
    number="${digits[0]}${digits[-1]}"

    sum=$((sum + number))
done < "$1"

echo "$sum"