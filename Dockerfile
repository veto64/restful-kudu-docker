FROM debian:jessie
# Install dependencies
RUN apt-get update
RUN apt-get -y install apt-utils wget dstat aptitude ntp supervisor

# Install repository and gpg key
WORKDIR /etc/apt/sources.list.d
RUN wget https://archive.cloudera.com/kudu/debian/jessie/amd64/kudu/archive.key -O archive.key
RUN apt-key add archive.key
RUN rm archive.key
RUN wget http://archive.cloudera.com/kudu/debian/jessie/amd64/kudu/cloudera.list
RUN apt-get update


# Install Kudu
RUN apt-get install -y apt-utils
RUN apt-get -y install libkuduclient0           # Kudu C++ client shared library
RUN apt-get -y install libkuduclient-dev # Kudu C++ client SDK

# Install tools to work inside the containers
RUN apt-get install -y emacs24-nox \
net-tools \
python-dev \
python-pip 

RUN pip install setuptools --upgrade 
RUN pip install cython
RUN pip install kudu-python==1.2.0 
RUN pip install falcon gunicorn  
RUN pip install PyYAML
RUN pip install falcon-cors


EXPOSE 80
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]



