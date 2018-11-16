FROM debian:jessie

# Install dependencies and tools
RUN apt-get update && apt-get -y install apt-utils \ 
wget \ 
dstat \ 
aptitude \ 
ntp \ 
emacs24-nox \
net-tools \
python-dev \
python-pip 

# Install repository and gpg key
WORKDIR /etc/apt/sources.list.d
RUN wget https://archive.cloudera.com/kudu/debian/jessie/amd64/kudu/archive.key -O archive.key
RUN apt-key add archive.key
RUN rm archive.key
RUN wget http://archive.cloudera.com/kudu/debian/jessie/amd64/kudu/cloudera.list

# Install Kudu # Kudu C++ client shared library # Kudu C++ client SDK
RUN apt-get update && apt-get -y install libkuduclient0  \ 
libkuduclient-dev \ 
libkrb5-dev  


RUN pip install setuptools --upgrade 
RUN pip install cython 
RUN pip install cython kudu-python==1.2.0 \ 
falcon \ 
gunicorn \ 
PyYAML \ 
falcon-cors


EXPOSE 80
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]



