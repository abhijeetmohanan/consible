FROM centos:7
RUN yum install epel-release -y
RUN yum install openssh-clients python-pip ansible -y
EXPOSE 22
CMD ["/usr/sbin/sshd -D"]
