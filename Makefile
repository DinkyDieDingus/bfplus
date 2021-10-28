SRC = bf/test.bf

.PHONY: test-asm test-bin test

test: test-asm.out test-bin.out

test-asm.out: ./src/compiler/asm.py
	./bfcomp.py $(SRC) -l asm -c test-asm.out
	hexdump -C test-asm.out > proper_dump.txt
	readelf test-asm.out -a > proper_elf.txt
	ndisasm -b64 -e 4096 test-asm.out > proper_disass.txt

test-bin.out: ./src/compiler/bin.py
	./bfcomp.py $(SRC) -l bin -c test-bin.out
	hexdump -C test-bin.out > my_dump.txt
	readelf test-bin.out -a > my_elf.txt
	ndisasm -b64 -e 120 test-bin.out > my_disass.txt

clean:
	rm -f *.c *.o *.out *.asm *.txt