FROM centos:7
RUN yum install python38 epel-release -y
RUN yum install python3-pip ansible openssh-clients -y
RUN python3 -m pip install --upgrade pip
RUN pip3 install  setuptools wheel flask docker ansible==2.7
WORKDIR /root/serverData/
COPY ./* /root/serverData/
CMD ["python3", "server_v1.py"]
EXPOSE 5000
