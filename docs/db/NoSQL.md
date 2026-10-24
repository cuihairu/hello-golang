###  NoSQL databases

#### 14.1 What is NoSQL

NoSQL (Not Only SQL) is an umbrella term for non-relational databases. The way data is stored and retrieved differs from relational databases like MySQL and PostgreSQL. Common characteristics:

- **Data model**: key-value, document, column-family, or graph — pick the one that matches how your application reads and writes.
- **Scaling**: scale out by adding nodes, aimed at large-scale data storage and high-concurrency access.
- **Read/write paths**: the storage layout is tuned for its own access pattern.
- **Replication and sharding**: provided by the database itself, used for data redundancy.

#### 14.2 Common NoSQL databases

##### MongoDB
MongoDB is a document-oriented NoSQL database that stores data as JSON-format documents. It supports a rich query language, indexes, and aggregation operations, and suits large-scale data storage and processing.

##### Redis
Redis is a key-value database that supports several data structures (strings, hashes, lists, sets, sorted sets, and so on). It is commonly used for caching, session management, and real-time analytics.

##### Example: installing and using MongoDB and Redis

**Installing MongoDB**
```bash
# on Ubuntu 18.04 you can install it straight with apt
sudo apt-get update
sudo apt-get install -y mongodb

# start MongoDB
sudo service mongodb start
```

Note: from Ubuntu 20.04 onward the official repositories no longer provide a `mongodb` package, so you need to add the `mongodb-org` apt repository following MongoDB's official instructions before installing.

**Installing Redis**
```bash
# install Redis on Ubuntu
sudo apt-get update
sudo apt-get install -y redis-server

# start Redis
sudo service redis-server start
```

#### 14.3 Using NoSQL databases in Go

##### Using MongoDB
To use MongoDB in Go, you can use the official `mongo-go-driver`.

**Installing the MongoDB driver**
```bash
go get go.mongodb.org/mongo-driver/mongo
```

**Example code: connecting to MongoDB and doing basic operations**
```go
package main

import (
    "context"
    "fmt"
    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
    "log"
)

func main() {
    clientOptions := options.Client().ApplyURI("mongodb://localhost:27017")
    client, err := mongo.Connect(context.TODO(), clientOptions)
    if err != nil {
        log.Fatal(err)
    }

    defer client.Disconnect(context.TODO())

    collection := client.Database("testdb").Collection("testcol")
    insertResult, err := collection.InsertOne(context.TODO(), map[string]string{"name": "John Doe"})
    if err != nil {
        log.Fatal(err)
    }

    fmt.Println("Inserted document:", insertResult.InsertedID)
}
```

##### Using Redis
To use Redis in Go, you can use the `redis/go-redis` library (formerly `go-redis/redis`, moved to the new path in v9).

**Installing the Redis driver**
```bash
go get github.com/redis/go-redis/v9
```

**Example code: connecting to Redis and doing basic operations**
```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/redis/go-redis/v9"
)

var ctx = context.Background()

func main() {
    rdb := redis.NewClient(&redis.Options{
        Addr:     "localhost:6379",
        Password: "", // no password set
        DB:       0,  // use default DB
    })

    err := rdb.Set(ctx, "key", "value", 0).Err()
    if err != nil {
        log.Fatal(err)
    }

    val, err := rdb.Get(ctx, "key").Result()
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("key", val)
}
```

#### 14.4 Comparing NoSQL and SQL databases

| Feature         | SQL database                          | NoSQL database                        |
| --------------- | ------------------------------------- | ------------------------------------- |
| Data model      | Relational model (tables, rows, columns) | Multiple models (key-value, document, column-family, graph) |
| Query language  | SQL                                   | Each database's own query API         |
| Transaction support | Strongly consistent transactions   | Most are eventually consistent        |
| Scalability     | Vertical scaling (adding hardware resources) | Horizontal scaling (adding nodes) |
| Use cases       | Complex queries, transactional work   | Large-scale data storage, high-concurrency access |
| Maintenance cost | Needs a DBA for complex database administration | Relatively low                  |

Choosing comes down to three things: does the data model fit how the application accesses data, do you need the strong consistency of transactions, and do you scale vertically or horizontally.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)


## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [Monitor](/db/Monitor.md)
- [Normalization](/db/Normalization.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Monitor](/db/Monitor.md)
- [Normalization](/db/Normalization.md)
