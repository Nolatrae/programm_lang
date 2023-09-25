all: run clean
	
run: build
	@./main

build: main.asm
	@nasm -f elf64 main.asm -o main.o
	@gcc -no-pie -fno-pie -o main main.o
	
clean:
	@rm -f main main.o
