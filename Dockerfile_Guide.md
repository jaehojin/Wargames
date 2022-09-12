# CTF를 위한 Dockerfile 실행방법

## [0] Docker 실행하기
```bash
sudo systemctl start docker
```

만약 환경이 WSL이거나, PID 1 에러가 뜬다면 다음 사항을 입력하면 된다.
```bash
sudo service docker start
```
* * *
## [1] Build & Images

Dockerfile은 Build를 해야 먼저 쓸 수 있다.
```bash
docker build -t <생성할 이미지명>:<태그명> <Dockerfile 위치>
```
- 생성할 이미지명: Dockerfile로 생성할 컨테이너 이미지의 이름
- 태그명: 보통 01, 02 등의 숫자
- Dockerfile 위치: Path 넣기

<br>
Build한 이미지는 다음 명령어를 통해 확인할 수 있다.

```bash
docker images
```

* * *
## [2] Run & PS
Dockerfile로 Build한 이미지는 Run을 통해 실행할 수 있다.
```bash
docker run (–name <컨테이너명>) (-d) (-p 8080:8080) (-v /root/centos/data:/data) <이미지명>:<태그명>
```
|태그|설명|
|:---:|:---:|
|--name|컨테이너명|
|-d|백그라운드 실행| 
|-p 8080:8080|포트포워딩- Local Port : Container Port|
|-v ():()|볼륨설정- 로컬경로 & 컨테이너경로 연결, <br> 파일 전송용도|

<br>
실행 중인 이미지는 다음 명령어를 통해 확인할 수 있다.

```bash
docker ps
```

* * *
## [3] 실행 및 접속
```bash
docker exec -it <컨테이너 ID> /bin/bash
```

컨테이너 종료 시 `exit` 입력 혹은 Ctrl+D를 누르면 된다.