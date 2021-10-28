#!/bin/bash
cut -c11- asm_hex.txt > cut_asm_hex.txt
cut -c11- bin_hex.txt > cut_bin_hex.txt
diff cut_asm_hex.txt cut_bin_hex.txt
rm cut_asm_hex.txt
rm cut_bin_hex.txt