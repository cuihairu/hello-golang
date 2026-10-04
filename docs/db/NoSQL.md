###  NoSQL数据库

#### 14.1 什么是NoSQL

NoSQL（Not Only SQL）是非关系型数据库的统称，数据的存取方式和MySQL、PostgreSQL这类关系型数据库不同，常见的特点有：

- **数据模型**：键值、文档、列族、图，按应用的存取方式选一种。
- **扩展方式**：加节点横向扩展，对应大规模数据存储和高并发访问。
- **读写路径**：为各自的访问模式优化存储结构。
- **复制与分片**：由数据库内置提供，用来做数据冗余。

#### 14.2 常见的NoSQL数据库

##### MongoDB
MongoDB是一种面向文档的NoSQL数据库，使用JSON格式的文档来存储数据。它支持丰富的查询语言、索引和聚合操作，适用于大规模数据存储和处理。

##### Redis
Redis是一种键值数据库，支持多种数据结构（字符串、哈希、列表、集合、有序集合等），常用于缓存、会话管理、实时分析。

##### 示例：MongoDB和Redis的安装和使用

**安装MongoDB**
```bash
# Ubuntu 18.04 可以直接用 apt 安装
sudo apt-get update
sudo apt-get install -y mongodb

# 启动MongoDB
sudo service mongodb start
```

注意：Ubuntu 20.04 之后的官方源已不再提供 `mongodb` 包，需要按 MongoDB 官网指引配置 `mongodb-org` 的 apt 源后再安装。

**安装Redis**
```bash
# Ubuntu安装Redis
sudo apt-get update
sudo apt-get install -y redis-server

# 启动Redis
sudo service redis-server start
```

#### 14.3 在Go中使用NoSQL数据库

##### 使用MongoDB
在Go中使用MongoDB，可以使用官方提供的`mongo-go-driver`。

**安装MongoDB驱动**
```bash
go get go.mongodb.org/mongo-driver/mongo
```

**示例代码：连接MongoDB并进行基本操作**
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

##### 使用Redis
在Go中使用Redis，可以使用 `redis/go-redis` 库（原 `go-redis/redis`，v9 起迁移到新路径）。

**安装Redis驱动**
```bash
go get github.com/redis/go-redis/v9
```

**示例代码：连接Redis并进行基本操作**
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

#### 14.4 NoSQL与SQL数据库的对比

| 特性          | SQL数据库                              | NoSQL数据库                             |
| ------------- | -------------------------------------- | --------------------------------------- |
| 数据模型      | 关系模型（表、行、列）                  | 多种模型（键值、文档、列族、图）         |
| 查询语言      | SQL                                    | 各自的查询API                          |
| 事务支持      | 强一致性事务                           | 大多数为最终一致性                     |
| 扩展性        | 垂直扩展（增加硬件资源）                | 水平扩展（增加节点）                    |
| 适用场景      | 复杂查询、事务性操作                    | 大规模数据存储、高并发访问              |
| 维护成本      | 需要DBA进行复杂的数据库管理              | 相对较低                                |

选型看三点：数据模型对不对得上应用的访问方式、要不要事务的强一致性、扩展走垂直还是水平。