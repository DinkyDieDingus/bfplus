#!/bin/bash

for file in bf/*; do
    make clean >/dev/null
    make SRC=$file >/dev/null 2>/dev/null
    if [ $? -ne 0 ]; then
        echo ✕ Failed $file
    else
        echo ✓ Passed $file
    fi
done

make clean >/dev/null