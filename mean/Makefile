all: run clean
run:
	@nasm -felf64 main.asm && ld main.o && ./a.out;
clean:
	@rm -f main.o a.out
