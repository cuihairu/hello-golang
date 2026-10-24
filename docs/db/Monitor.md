### Database monitoring and logging

Monitoring tells you what the database is doing right now; logs record the operations and events that already happened. When a performance bottleneck or a fault shows up, the former gets you there early, the latter lets you trace exactly what happened.

#### 19.1 The importance of database monitoring

Database monitoring is continuous observation of the running state. Slow queries, lock waits, resource pressure - problems of this kind only become something you can optimize or fix once they show up in monitoring. It mainly keeps an eye on four things:

- **Performance optimization**: use monitoring metrics to identify bottlenecks, and optimize queries and database configuration.
- **Troubleshooting**: catch errors and anomalies early, and pin down their cause quickly.
- **Capacity planning**: monitor how database resources are used, providing data to support future capacity expansion.
- **Security auditing**: record database access and operation logs to keep data safe.

#### 19.2 Key monitoring metrics

The common monitoring metrics fall into these categories, each corresponding to the database's performance or health:

- **Query performance**: query response time, throughput, slow queries, and so on.
- **Connections**: current active connections, maximum connections, connection-pool usage, and so on.
- **Resource usage**: CPU utilization, memory utilization, disk I/O, network I/O, and so on.
- **Cache hit rate**: the hit and miss rate of the database cache.
- **Lock waits**: lock wait time, deadlocks, and so on.
- **Transaction handling**: number of commits and rollbacks, transaction response time, and so on.

#### 19.3 Common database monitoring tools

##### 19.3.1 Prometheus

Prometheus is an open-source monitoring system and time-series database. It supports multiple data-collection methods and query languages; database metrics are pulled, stored, and queried by it.

##### 19.3.2 Grafana

Grafana is an open-source data visualization tool. Once you connect a data source like Prometheus, it renders monitoring metrics as charts and dashboards.

##### 19.3.3 MySQL Performance Schema

MySQL Performance Schema is MySQL's built-in performance monitoring tool. It collects detailed runtime performance data from the database, including query performance, lock waits, and resource usage.

##### 19.3.4 pg_stat_statements

pg_stat_statements is an extension module for PostgreSQL. It records and analyzes how SQL queries execute, including query frequency, response time, and execution plan.

#### 19.4 Implementing database monitoring in Go

In Go, you can use the Prometheus client library to monitor the database and expose the monitoring data to Prometheus for collection and analysis.

##### 19.4.1 Installing the Prometheus client library

```bash
go get github.com/prometheus/client_golang/prometheus
go get github.com/prometheus/client_golang/prometheus/promhttp
```

##### 19.4.2 Defining monitoring metrics

Define the metrics you want to monitor in Go code:
```go
var (
    queryDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "db_query_duration_seconds",
            Help:    "Duration of database queries.",
            Buckets: prometheus.DefBuckets,
        },
        []string{"query"},
    )
    activeConnections = prometheus.NewGauge(
        prometheus.GaugeOpts{
            Name: "db_active_connections",
            Help: "Number of active database connections.",
        },
    )
)

func init() {
    prometheus.MustRegister(queryDuration, activeConnections)
}
```

##### 19.4.3 Collecting monitoring data

Collect monitoring data during database operations:
```go
func executeQuery(query string, db *sql.DB) {
    start := time.Now()
    _, err := db.Exec(query)
    duration := time.Since(start).Seconds()

    queryDuration.WithLabelValues(query).Observe(duration)

    if err != nil {
        log.Printf("Query failed: %v", err)
    }
}
```

##### 19.4.4 Exposing monitoring data

Expose the monitoring data to Prometheus for collection:
```go
http.Handle("/metrics", promhttp.Handler())
log.Fatal(http.ListenAndServe(":8080", nil))
```

#### 19.5 Database logs

Database logs are an important tool for recording database operations and events. Through logs you can track the running state, query execution, security events, and more.

##### 19.5.1 Common database log types

- **Error log**: records errors and exceptions that occur at runtime.
- **Query log**: records every SQL query executed, usually for auditing and analysis.
- **Slow query log**: records slow queries whose execution time exceeds a set threshold, to make performance optimization easier.
- **Transaction log**: records transaction commits and rollbacks, used for recovery after a fault.

##### 19.5.2 Recording database logs in Go

In Go, you can use the standard library's log package or a third-party logging library (such as Logrus or Zap) to record database operation logs.

```go
package main

import (
    "database/sql"
    "log"
    "os"

    _ "github.com/go-sql-driver/mysql"
    "github.com/sirupsen/logrus"
)

func main() {
    // set up log output
    logFile, err := os.OpenFile("db.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
    if err != nil {
        log.Fatal(err)
    }
    logrus.SetOutput(logFile)
    logrus.SetFormatter(&logrus.TextFormatter{
        FullTimestamp: true,
    })

    // connect to the database
    db, err := sql.Open("mysql", "user:password@tcp(localhost:3306)/dbname")
    if err != nil {
        logrus.WithError(err).Fatal("Failed to connect to database")
    }
    defer db.Close()

    // execute a query
    query := "SELECT * FROM users"
    rows, err := db.Query(query)
    if err != nil {
        logrus.WithError(err).WithField("query", query).Error("Failed to execute query")
        return
    }
    defer rows.Close()

    logrus.WithField("query", query).Info("Query executed successfully")
}
```

#### 19.6 Log analysis and management

##### 19.6.1 Log analysis

By analyzing database logs, you can spot performance bottlenecks, error patterns, and security events. Common log-analysis tools include the ELK (Elasticsearch, Logstash, Kibana) stack and Splunk.

##### 19.6.2 Log management

Effective log management covers log storage, archiving, and cleanup policies. You need to archive and clean up old logs regularly, so that log files do not grow so large that they hurt performance.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)


## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [Mock](/db/Mock.md)
- [NoSQL](/db/NoSQL.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Mock](/db/Mock.md)
- [NoSQL](/db/NoSQL.md)
