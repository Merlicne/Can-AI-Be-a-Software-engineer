#!/bin/bash

# Read the Project_structure.txt file
while IFS= read -r line; do
    # Create the directory
    if [[ $line == */ ]]; then
        mkdir -p "$line"
    else
        # Create the file
        touch "$line"
    fi
done < "Project_structure.txt"