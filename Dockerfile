FROM jobber:latest

USER root
ENV USERID=0
WORKDIR /root

RUN apk add python3 py3-pip tzdata && \
    pip3 install pyyaml boto3

ENV TZ=America/Toronto

COPY init.py backup.py /root/

RUN rm /home/jobberuser/.jobber && \
    mkdir /var/jobber/0 && \
    touch /root/empty-script && \
    chmod +x /root/empty-script /root/init.py /root/backup.py

CMD [ "sh","-c","/root/init.py && /usr/libexec/jobberrunner -u /var/jobber/0/cmd.sock /root/.jobber"]