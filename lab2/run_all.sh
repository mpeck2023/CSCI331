#!/bin/bash

output_file="results.txt"
> "$output_file" 
files=$(find . -type f -name "*.cnf")

for file in $files; do
    filename=$(basename "$file")
    result=$(py lab2.py "$file")
    echo "$filename" >> output_file
    echo "$result" >> output_file
done