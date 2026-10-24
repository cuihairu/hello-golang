###  High availability and backup

#### 13.1 Designing a highly available architecture

High availability has a straightforward goal: when the database fails, the service does not go down and downtime stays short. There are four common approaches:

- **Master-slave replication**: set up master and slave database servers to replicate data in real time and provide redundancy, improving the system's fault tolerance.
- **Load balancing**: use a load balancer to distribute database requests, avoiding single points of failure and improving availability.
- **Automatic failover**: when the master database server fails, switch over to a standby server automatically to keep the service running.
- **Multi-region deployment**: deploy the database across multiple geographic regions to guard against single points of failure and regional disasters.

##### Example: MySQL master-slave replication configuration
1. Configure the master server:
```sql
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog-do-db = your_database_name
```

2. Configure the slave server:
```sql
[mysqld]
server-id = 2
relay-log = mysql-relay-bin
```

3. Create a replication user on the master server:
```sql
CREATE USER 'replicator'@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO 'replicator'@'%';
```

4. Start replication on the slave server:
```sql
CHANGE MASTER TO
    MASTER_HOST='master_host',
    MASTER_USER='replicator',
    MASTER_PASSWORD='password',
    MASTER_LOG_FILE='mysql-bin.000001',
    MASTER_LOG_POS=  4;
START SLAVE;
```

#### 13.2 Database backup strategies

The purpose of a backup is straightforward: if the data is lost, you can get it back; after a fault, you can recover. There are three common backup strategies:

- **Full backup**: back up the entire database completely, suitable for an initial backup and for periodic complete backups.
- **Incremental backup**: back up only the data that has changed since the last backup, saving storage space and time.
- **Differential backup**: back up all changes since the last full backup, falling between a full backup and an incremental backup.

##### Example: a full backup using `mysqldump`
```bash
mysqldump -u user -p your_database_name > backup.sql
```

##### Example: an incremental backup using `mysqldump`
```bash
mysqldump -u user -p --single-transaction --flush-logs --master-data=2 your_database_name > incremental_backup.sql
```

#### 13.3 Recovery and disaster recovery

When the database fails or data is lost, backups and a plan laid down in advance bring the service back. The steps include:

- **Verify backups**: periodically verify the integrity and usability of backups, making sure the backup files can be restored.
- **Restore data**: restore the data from a backup file according to your backup strategy.
- **Disaster recovery**: draw up a detailed disaster recovery plan covering the whole process, from restoring backups to troubleshooting to bringing the business back up.

##### Example: restoring data from a `mysqldump` backup file
```bash
mysql -u user -p your_database_name < backup.sql
```

#### 13.4 Distributed databases and clusters

Distributed databases and cluster technology spread data across multiple nodes to achieve data redundancy and high availability. Common distributed database and cluster solutions include:

- **Master-slave replication cluster**: use master-slave replication to synchronize data to multiple slaves, improving data availability and read/write performance.
- **Sharded cluster**: shard the database so that each node stores only part of the data, suitable for large-scale data storage and high-concurrency access.
- **Fault-tolerant cluster**: use a fault-tolerance mechanism such as consensus algorithms like Raft and Paxos, to guarantee data consistency and high availability.

##### Example: configuring a MongoDB sharded cluster
1. Start the config server:
```bash
mongod --configsvr --replSet configReplSet --dbpath /data/configdb --port 27019
```

2. Start the shard server:
```bash
mongod --shardsvr --replSet shardReplSet --dbpath /data/shard1 --port 27018
```

3. Start the router:
```bash
mongos --configdb configReplSet/localhost:27019 --port 27017
```

4. Add a shard:
```javascript
sh.addShard("shardReplSet/localhost:27018")
```

This page records four things: the MySQL master-slave replication configuration, full and incremental backups with `mysqldump`, the command for restoring data from a backup file, and the steps for starting a MongoDB sharded cluster.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)

## Sibling pages

- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [GraphQL](/db/GraphQL.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [GraphQL](/db/GraphQL.md)
- [Install](/db/Install.md)
- [Lib](/db/Lib.md)
- [Migrate](/db/Migrate.md)
- [Mock](/db/Mock.md)
- [Monitor](/db/Monitor.md)
- [NoSQL](/db/NoSQL.md)
- [Normalization](/db/Normalization.md)
- [ORM](/db/ORM.md)
- [Performance](/db/Performance.md)
- [Project](/db/Project.md)
- [Readme](/db/Readme.md)
- [SQL](/db/SQL.md)
- [Security](/db/Security.md)
- [Sharding](/db/Sharding.md)
- [Tx](/db/Tx.md)
