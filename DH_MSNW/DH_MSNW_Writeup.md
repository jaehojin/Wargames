# DreamHack MSNW WriteUp

    문제 분야: Pwnable
    Dreamhack Level: Level 1
    Keyword: Frame Pointer Overflow, String Leak, Stack Frame

> 이 문제는 MSNW (Meong Said, Nyang Wrote) 프로그램이 서비스로 등록되어 동작하고 있습니다. <br>
프로그램의 취약점을 찾고 익스플로잇해 플래그를 획득하세요! <br >
플래그 형식은 DH{…} 입니다.

* * *
## 1. Caller-Callee 구조 살펴보기

이번 프로그램은 Caller와 Callee 함수가 서로 엮여있는 관계가 있다.

이 프로그램의 구조는 다음과 같다.

    Main -> Echo -> ( Call -> Meong )
    -> Echo -> ( Call -> Nyang )
    -> Echo -> ( Call -> Meong ) -> ...

사용자가 문자 q를 입력하지 않으면, 프로젝트 이름처럼 Meong에서 입력받고, Nyang에서 출력하는 간단한 구조의 프로그램이다.

더 자세히 살펴보자면, *msnw.c* 파일에서도 알 수 있듯이, Echo 함수 내부에서 *Call(Meong)* 과 *Call(Nyang)* 이 while 루프로 반복되는 구조를 가지고 있다. 함수명 그대로, Call 함수가 **Caller**, Meong과 Nyang 함수가 **Callee** 성격을 띠게 된다.

각 함수의 디스어셈블된 결과는 다음과 같다.

### **Call 함수**
```as
0x00000000004012f8 <+0>:     endbr64 
0x00000000004012fc <+4>:     push   rbp
0x00000000004012fd <+5>:     mov    rbp,rsp
0x0000000000401300 <+8>:     sub    rsp,0x1f0 // 주목
0x0000000000401307 <+15>:    mov    DWORD PTR [rbp-0xf4],edi
0x000000000040130d <+21>:    cmp    DWORD PTR [rbp-0xf4],0x0
0x0000000000401314 <+28>:    jne    0x401322 <Call+42>
0x0000000000401316 <+30>:    mov    eax,0x0
0x000000000040131b <+35>:    call   0x401242 <Meong>
0x0000000000401320 <+40>:    jmp    0x40132c <Call+52>
0x0000000000401322 <+42>:    mov    eax,0x0
0x0000000000401327 <+47>:    call   0x4012b0 <Nyang>
0x000000000040132c <+52>:    leave  
0x000000000040132d <+53>:    ret
```

### **Meong 함수**
```as
0x0000000000401242 <+0>:     endbr64 
0x0000000000401246 <+4>:     push   rbp
0x0000000000401247 <+5>:     mov    rbp,rsp
0x000000000040124a <+8>:     sub    rsp,0x1f0 // 주목
0x0000000000401251 <+15>:    lea    rax,[rbp-0x130]
0x0000000000401258 <+22>:    mov    edx,0x130
0x000000000040125d <+27>:    mov    esi,0x0
0x0000000000401262 <+32>:    mov    rdi,rax
0x0000000000401265 <+35>:    call   0x4010b0 <memset@plt>
0x000000000040126a <+40>:    lea    rax,[rip+0xd93]        # 0x402004
0x0000000000401271 <+47>:    mov    rdi,rax
0x0000000000401274 <+50>:    mov    eax,0x0
0x0000000000401279 <+55>:    call   0x4010a0 <printf@plt>
0x000000000040127e <+60>:    lea    rax,[rbp-0x130]
// mov rsi, rax를 통해 buf의 주소인 것을 알 수 있다.
0x0000000000401285 <+67>:    mov    edx,0x132
// buf의 크기인 0x132보다 크므로 Overflow 가능
0x000000000040128a <+72>:    mov    rsi,rax
// rax(=buf)가 read의 2번째 인자인 rsi로 가는 모습
0x000000000040128d <+75>:    mov    edi,0x0
0x0000000000401292 <+80>:    call   0x4010c0 <read@plt>
0x0000000000401297 <+85>:    movzx  eax,BYTE PTR [rbp-0x130]
0x000000000040129e <+92>:    cmp    al,0x71
0x00000000004012a0 <+94>:    jne    0x4012a9 <Meong+103>
0x00000000004012a2 <+96>:    mov    eax,0x0
0x00000000004012a7 <+101>:   jmp    0x4012ae <Meong+108>
0x00000000004012a9 <+103>:   mov    eax,0x1
0x00000000004012ae <+108>:   leave  
0x00000000004012af <+109>:   ret
```

### **Nyang 함수**
```as
0x00000000004012b0 <+0>:     endbr64 
0x00000000004012b4 <+4>:     push   rbp
0x00000000004012b5 <+5>:     mov    rbp,rsp
0x00000000004012b8 <+8>:     sub    rsp,0x1f0 // 주목
0x00000000004012bf <+15>:    lea    rax,[rip+0xd4b]        # 0x402011
0x00000000004012c6 <+22>:    mov    rdi,rax
0x00000000004012c9 <+25>:    mov    eax,0x0
0x00000000004012ce <+30>:    call   0x4010a0 <printf@plt>
0x00000000004012d3 <+35>:    lea    rax,[rbp-0x130]
// 0x130 크기의 공간 -> Meong의 buf 시작 주소와 동일
0x00000000004012da <+42>:    mov    rsi,rax
0x00000000004012dd <+45>:    lea    rax,[rip+0xd3a]        # 0x40201e
0x00000000004012e4 <+52>:    mov    rdi,rax
0x00000000004012e7 <+55>:    mov    eax,0x0
0x00000000004012ec <+60>:    call   0x4010a0 <printf@plt>
0x00000000004012f1 <+65>:    mov    eax,0x1
0x00000000004012f6 <+70>:    leave  
0x00000000004012f7 <+71>:    ret 
```

## 2. Frame Pointer Overflow
일반적인 ROP라면 Return Address를 덮어버리는 공격이었을 텐데, 이번 프로그램은 Meong 함수의 스택프레임에서 `buf의 시작주소부터 Old %rbp의 2바이트까지만` 덮어버린다. 이 때문에 우리는 타겟을 Return Address가 아니라 `%rbp` 에 맞춰야 한다.

Frame Pointer Overflow는 간단히 말하자면 

그러나 이 공격은

1. 서브함수가 존재
2. ASLR로 인해 영향받는 부분 회피
3. 

의 필수조건을 가지고 있다.

ASLR이 Old %rbp 주소를 원하는 위치로 Overwrite 하는 데에 큰 지장을 주지만, 다행히도 우리는 주어진 *Nyang 함수*를 통해서 `의도치 않게 출력되는 RBP 주소를 Leak`할 수 있다.

## 3. Old RBP Leak

## 4. FPO 구현

## 5. Exploit
