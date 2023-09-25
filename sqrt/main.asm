section .data
  value dd 81
	format db "%d", 0xA

section .text
	global main
	extern printf

main: 
  fild dword [value]
  fsqrt
  fistp dword [res]

print:
  push rax
  push rbx
  push rcx
  push rdx
  push rbp
  mov rdi, format
  mov rsi, [res]
  call printf
  pop rax
  pop rbx
  pop rcx
  pop rdx
  pop rbp

end:
  mov rax, 60
  xor rdi, rdi
  syscall

section .bss
  res resb 1