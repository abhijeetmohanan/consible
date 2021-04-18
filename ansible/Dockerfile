FROM centos:7
RUN yum install epel-release -y
RUN yum install openssh-clients python-pip ansible -y
WORKDIR $HOME/ansible/
ADD key_create.sh
ENTRYPOINT ["sh", "deploy.sh"]
