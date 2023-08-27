FROM ubuntu:18.04

RUN apt update
RUN apt install -y xinetd
RUN useradd ctf

RUN mkdir /home/ctf
ADD bin /home/ctf/bin
ADD run.sh /home/ctf/run.sh
ADD flag /flag

RUN chmod 460 /home/ctf/*
RUN chown ctf:root /home/ctf/*
RUN chmod +x /home/ctf/bin
RUN chmod +x /home/ctf/run.sh
RUN chmod 555 /flag

ADD xinetd /etc/xinetd.d/
EXPOSE 5555

CMD ["/usr/sbin/xinetd","-dontfork"]
