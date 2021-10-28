SRC = bf/test.bf
BIN_OFFSET = 120
ASM_OFFSET = 4096

.PHONY: test

test: asm_hex.txt asm_elf.txt asm_dis.txt bin_hex.txt bin_elf.txt bin_dis.txt
	./test-diff.sh

asm.out: ./src/compiler/asm.py $(SRC)
	./bfcomp.py $(SRC) -l asm -c asm.out

asm_hex.txt: asm.out bin.out
	hexdump -C asm.out -s $(ASM_OFFSET) -n $$(($$(wc -c < bin.out) - 120)) > asm_hex.txt

asm_elf.txt: asm.out
	readelf asm.out -a > asm_elf.txt

asm_dis.txt: asm.out bin_dis.txt
	( ndisasm -b64 -e $(ASM_OFFSET) asm.out | head -n $$(wc -l < bin_dis.txt) ) > asm_dis.txt

bin.out: ./src/compiler/bin.py $(SRC)
	./bfcomp.py $(SRC) -l bin -c bin.out

bin_hex.txt: bin.out
	hexdump -C bin.out -s $(BIN_OFFSET) > bin_hex.txt

bin_elf.txt: bin.out
	readelf bin.out -a > bin_elf.txt

bin_dis.txt: bin.out
	ndisasm -b64 -e $(BIN_OFFSET) bin.out > bin_dis.txt

clean:
	rm -f *.c *.o *.out *.asm *.txt