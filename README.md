# Python Falcon API for a Kudu ServerB

The main repository is on:
[https://calantas.org/kudu-docker/](https://calantas.org/restful-kudu-docker)

![logo](http://getkudu.io/img/logo.png)

## License
GNU General Public License v3.0 -

## What is Kudu?
Kudu is an open source storage engine for structured data which supports low-latency random access together with effi- cient analytical access patterns. Kudu distributes data using horizontal partitioning and replicates each partition using Raft consensus, providing low mean-time-to-recovery and low tail latencies. Kudu is designed within the context of the Hadoop ecosystem and supports many modes of access via tools such as [Cloudera Impala](http://impala.io/), [Apache Spark](http://spark.apache.org/), and [MapReduce](https://hadoop.apache.org/).

[http://kudu.apache.org/](http://kudu.apache.org/)

## Startup 

1. use the docker composer to start the API server with 1 queen(master) and 3 slaves(tablet/region servers), they all are in the same network for the moment.
```bash
docker-compose up 
```






### Web UI
| Control Websiste               | Port                                              |
| ----------------------- |-------------------------------------------------- |
| API                     | [http://127.0.0.1:80](http://127.0.0.1:80)  |
| Landing                 | [http://127.0.0.1:8051](http://127.0.0.1:8051)  |
| View Slaves/Tablets     | [http://127.0.0.1:8051/tablet-servers](http://127.0.0.1:8051/tablet-servers)  |



