section .data
  minsym db "-"
  new db 0xA, 0xD

  x dd 5, 3, 2, 6, 1, 7, 4
  xlen equ ($-x) / 4

  y dd 0, 10, 1, 9, 2, 8, 5
  ylen equ ($-y) / 4

section .bss
  result resd 1

section .text
  global _start

_start:
  mov rcx, xlen
  call diff_array

  mov rcx, xlen
  call get_average

  jmp end

get_average:
  xor rbx, rbx

  .sum_loop:
    mov dx, [x+rbx*4]
    add [x+rbx*4+4], dx

    inc rbx

    loop .sum_loop

  xor rax, rax
  xor rdx, rdx
  movsx rax, byte [x+rbx*4]
  test rax, rax

  js .negative

  .positive:
    div rbx
    mov [result], rax
    jmp .finish

  .negative: 
    neg rax
    div rbx
    mov [result], rax
    mov rsi, minsym
    call print
    jmp .finish
    
  .finish:
    mov rsi, result 
    add [rsi], byte '0'
    call print

    mov rsi, new
    call print
    ret

diff_array: 
  xor rbx, rbx

  .diff_loop:
    mov ah, [y+rbx*4]
    sub [x+rbx*4], ah
    inc rbx
    loop .diff_loop
    ret

print: 
  mov rax, 1
  mov rdi, 1
  mov rdx, 1
  syscall
  ret

end: 
  mov rax, 60
  xor rdi, rdi
  syscall