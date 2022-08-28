# Zero Gravity Write-up
## 2022 Fall GoN CTF

### [1] Loop 횟수 늘리기
IDA Hex-ray로 디어셈블링을 해보면 다음과 같은 결과가 나온다. 참고로 이 코드는 main 함수 내부의 코드의 일부이며, arr 배열과 cnt는 전역변수이다.
```c
cnt = 1;
  init_main(argc, argv, envp);
  for ( i = 0; i < cnt; ++i )
  {
    printf("(r)ead / (a)dd >> ");
    __isoc99_scanf("%2s", &letter);
    if ( (char)letter == 'a' )
    {
      printf(" idx >> ");
      __isoc99_scanf("%d", &idx);
      printf(" value >> ");
      __isoc99_scanf("%f", &value);
      arr[idx] = value + arr[idx];
    }
    else if ( (char)letter == 'r' )
    {
      printf(" idx >> ");
      __isoc99_scanf("%d", &idx);
      printf("%.10e\n", arr[idx]);
    }
    memset(&letter, 0, 3uLL);
  }
  return 0;
```

read와 add를 반복하면서 진행하는 바이너리 파일인데, for 루프가 딱 1번 진행되기 때문에 cnt의 값을 바꿔줘야 한다.

bss 영역에 있는 전역변수 arr과 cnt의 메모리 주소는 다음과 같았다.

- arr: 0x6010A0
- cnt: 0x6010E0

arr 배열은 16개의 float 자료형을 담는 배열이고, arr의 float와 cnt의 자료형인 int 모두 4byte이다. 그러므로, **Out of Bounds(OOB)** 를 활용하여 cnt를 건드릴 수 있다.

    arr                                   cnt
    |0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|

처음에 add 옵션을 활용하여, 16번째 idx에 원하는 만큼의 루프 횟수를 넣어 변경해준다.

* * *

## [2] 