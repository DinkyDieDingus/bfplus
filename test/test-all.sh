#!/bin/bash
# test-all.sh
# Runs a test suites which tests that the handmade binaries for
# all bf source files in bf/ match the binaries produced by nasm

quiet=">/dev/null"
quiet2=">/dev/null"
if [ -n "$1" ]; then
    if [ $1 == "-v" ]; then
        quiet=""
        quiet2=""
    fi
fi

for file in ../bf/*; do
    eval "make clean $quiet"
    eval "make SRC=$file $quiet $quiet2"
    if [ $? -ne 0 ]; then
        echo ✕ Failed $file
    else
        echo ✓ Passed $file
    fi
done

eval "make clean $quiet"