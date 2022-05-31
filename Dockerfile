FROM kalilinux/kali-rolling

RUN apt update
RUN apt install vim firefox-esr openssh-server bash xauth sudo -y

COPY sshd.sh /
RUN chmod u+x /sshd.sh
RUN ssh-keygen -A

RUN rm /etc/ssh/sshd_config
COPY sshd_config /etc/ssh/sshd_config

RUN service ssh start

RUN useradd --home /home/kali --create-home --shell /bin/bash kali
RUN echo 'kali:kali' | chpasswd
RUN echo "kali ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]