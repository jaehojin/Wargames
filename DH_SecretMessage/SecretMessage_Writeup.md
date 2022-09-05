# Secret Message Writeup
## Dreamhack CTF Season 1 Round #9

**문제 정보**

    Category: Reversing

    드림이는 비밀스런 이미지 파일을 자신이 공부한 알고리즘을 통해 인코딩 하였어요.

    인코딩 프로그램을 분석하여 원본 이미지를 알아내주세요.

    원본 파일을 구한 경우 imageviewer.py를 통해 이미지를 볼 수 있습니다.

* * *
## [1] Binary File 리버싱

IDA Hex-Ray를 통해서 바이너리 파일 prob을 리버싱한 결과는 다음과 같다. 변수들의 경우, 맥락에 따라 이름을 다시 지정했다.

**main 함수**
```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  FILE *raw_rb; // [rsp+0h] [rbp-10h]
  FILE *enc_wb; // [rsp+8h] [rbp-8h]

  raw_rb = fopen("secretMessage.raw", "rb");
  enc_wb = fopen("secretMessage.enc", "wb");
  convertImage(raw_rb, enc_wb);
  remove("secretMessage.raw");
  puts("done!");
  fclose(enc_wb);
  fclose(raw_rb);
  return 0LL;
}
```

**convertImage 함수**
```c
__int64 __fastcall convertImage(FILE *raw, FILE *enc)
{
  unsigned __int8 count; // [rsp+17h] [rbp-9h]
  int cnt_pixel; // [rsp+18h] [rbp-8h]
  int previous; // [rsp+1Ch] [rbp-4h]

  if ( raw && enc )
  {
    previous = -1;
    count = 0;
    while ( 1 )
    {
      cnt_pixel = fgetc(raw);
      if ( cnt_pixel == -1 )
        return 0LL;
      fputc(cnt_pixel, enc);
      if ( cnt_pixel == previous )
      {
        count = 0;
        while ( 1 )
        {
          cnt_pixel = fgetc(raw);
          if ( cnt_pixel == -1 )                // EOF
            break;
          if ( cnt_pixel != previous )
          {
            fputc(count, enc);
            fputc(cnt_pixel, enc);
            previous = cnt_pixel;
            break;
          }
          if ( ++count == 0xFF )
          {
            fputc(255, enc);
            previous = -1;
            break;
          }
        }
      }
      else
      {
        previous = cnt_pixel;
      }
      if ( cnt_pixel == -1 )
      {
        fputc(count, enc);
        return 0LL;
      }
    }
  }
  else
  {
    *__errno_location() = 2;
    return 0xFFFFFFFFLL;
  }
}
```

prob 파일을 보면, raw 파일을 enc 파일로 변환해준 다음에 raw 파일을 삭제하고 끝난다.

변환 과정은,

1. raw 파일에서 현재 index에 있는 값을 enc 파일에 넣는다.
2. 만약 이전 index에 있는 값과 동일하면, 그 다음 index를 순차적으로 비교한다.
3. 그 다음 index도 동일하면 count 변수로 동일한 값들의 수를 세면서 무시해버린다.
4. 다른 값이 나왔을 경우, 동일한 값들의 수를 센 변수인 count 변수의 값을 넣고 진행한다.

```c
if ( ++count == 0xFF )
    {
    fputc(255, enc);
    previous = -1;
    break;
    }
```
count 변수가 왜 갑자기 튀어나오나 했는데, 절차적 프로그래밍의 특성 상 if의 조건문을 건드릴 수밖에 없게 되고, for 루프를 돌 때마다 무조건 count는 하나씩 증가하는 것을 볼 수 있었다.

따라서 우리가 만들어야 하는 것은, 변환된 enc 파일을, 변환 알고리즘의 반대 과정을 거치는 알고리즘을 적용하여, 다시 raw 파일을 만들어야 한다는 것이다. 즉, Decoding 알고리즘을 만들어야 한다는 것이다.

* * *
## [2] Decoding 알고리즘 제작

**converter.py**
```python
enc = open("./secretMessage.enc", "rb")
raw = open("./secretMessage.raw", "wb")

enc_image = bytes(enc.read())
secretMessage = b""
print(enc_image)

width = 500
height = 50
size = width * height

prv_pixel = -1
checked = False
for idx in range(len(enc_image)):
	if checked:
		checked = False
		prv_pixel = -1
		continue
	cnt_pixel = enc_image[idx].to_bytes(1, 'little')
	secretMessage += cnt_pixel
	if idx > 0 and prv_pixel == cnt_pixel:
		count = enc_image[idx+1]
		for num in range(count):
        		secretMessage += cnt_pixel
		checked = True
	prv_pixel = cnt_pixel

print(secretMessage)
print(len(secretMessage))

raw.write(secretMessage)

enc.close()
raw.close()
```

문제와 같이 주어진 imageviewer.py는 500x50 사이즈의 이미지를 보여주는데, 길이가 3000 정도밖에 되지 않는 raw 이미지를 어떻게 보여주는지는 잘 모르겠다.

converter.py는 Decoding 알고리즘을 만들어서 raw 파일을 제작하는 코드이다.

* * *
## [3] Output
