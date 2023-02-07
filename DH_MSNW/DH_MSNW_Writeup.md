# DreamHack MSNW WriteUp

    문제 분야: Pwnable
    Dreamhack Level: Level 1

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

*msnw.c* 파일에서도 알 수 있듯이, Meong 함수에 'q'가 입력되었는지 여부에 따라 *Call(Meong)* 과 *Call(Nyang)* 이 while문에서 반복되는 구조를 가지고 있다. 

각 함수의 디스어셈블된 결과는 다음과 같다.

## Call 함수
```as
0x00000000004012f8 <+0>:     endbr64 
0x00000000004012fc <+4>:     push   rbp
0x00000000004012fd <+5>:     mov    rbp,rsp
0x0000000000401300 <+8>:     sub    rsp,0x1f0
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