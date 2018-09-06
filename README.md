# Debian based Docker image for Kudu with 3 slaves

The main repository is on:
[https://calantas.org/kudu-docker/](https://calantas.org/kudu-docker)

![logo](http://getkudu.io/img/logo.png)

## License
GNU General Public License v3.0 -

## What is Kudu?
Kudu is an open source storage engine for structured data which supports low-latency random access together with effi- cient analytical access patterns. Kudu distributes data using horizontal partitioning and replicates each partition using Raft consensus, providing low mean-time-to-recovery and low tail latencies. Kudu is designed within the context of the Hadoop ecosystem and supports many modes of access via tools such as [Cloudera Impala](http://impala.io/), [Apache Spark](http://spark.apache.org/), and [MapReduce](https://hadoop.apache.org/).

[http://kudu.apache.org/](http://kudu.apache.org/)

## Startup 

1. use docker composer to start 1 queen(master) and 3 slaves(tablet/region servers)
```bash
docker-compose up 
```
or as deamon
```bash
docker-compose up -d
```

2.
for testing excecute the file test.sh or  
```bash

docker run --network=kudu-docker_queen  --rm -v "`pwd`:/opt/test"  veto64/kudu-docker /usr/bin/python /opt/test/main.py
```bash

because the dockers network name rename itself on different versions check the used network name, so use the right parameter
-network=kudu-docker_queen

with:  
```bash
docker network list
```bash






### Web UI
| Control Websiste               | Port                                              |
| ----------------------- |-------------------------------------------------- |
| Landing                 | [http://127.0.0.1:8051](http://127.0.0.1:8051)  |
| View Slaves/Tablets     | [http://127.0.0.1:8051/tablet-servers](http://127.0.0.1:8051/tablet-servers)  |



