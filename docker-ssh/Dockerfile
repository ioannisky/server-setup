FROM ubuntu:14.04
RUN apt-get update && apt-get install -y openssh-server && rm -rf /var/lib/apt/lists/*

COPY ./local_test_rsa.pub /root/.ssh/authorized_keys

RUN chmod 644 /root/.ssh/authorized_keys
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

COPY run.sh /opt/run.sh
RUN chmod u+x /opt/run.sh

COPY list_keys.sh /opt/list_keys.sh
RUN chmod u+x /opt/list_keys.sh

RUN mkdir /var/run/sshd && chmod 0755 /var/run/sshd


EXPOSE 22

CMD ["/opt/run.sh"]
