### Performance optimization

#### 10.1 Principles of database performance optimization

Optimization starts in three places: the database structure, indexes, and the SQL itself. Keep the structure normalized to avoid data redundancy; indexes speed queries up noticeably, but every index adds overhead to writes, so they must not be added without limit; keep the query statements free of unnecessary complexity. Two other routine matters are the connection pool (cuts the cost of creating and destroying connections) and caching (cuts how often the database is hit).

#### 10.2 Using indexes to optimize queries

Indexes are the most common tool in database optimization. Put an index on the columns used in the query conditions, and the database no longer has to scan the whole table.

Example:
```sql
CREATE INDEX idx_users_email ON users(email);
```

This way, when querying the `email` column of the `users` table, the database can use the index to locate the data quickly:
```sql
SELECT * FROM users WHERE email = 'example@example.com';
```

#### 10.3 Types and use of indexes

Databases have several types of indexes, each suited to different scenarios:

- **Single-column index**: an index created on a single column, the most common type.
- **Multi-column index**: an index created on multiple columns, which can optimize queries with more than one condition.
- **Unique index**: ensures the values in the indexed column are unique, commonly used for unique constraints.
- **Fulltext index**: used to speed up text search operations.
- **Hash index**: an index implemented with a hash table, suitable for equality queries.

Example:
```sql
CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE FULLTEXT INDEX idx_users_bio ON users(bio);
```

#### 10.4 Query analysis and optimization

The first step in optimizing a query is to analyze its execution plan. From the execution plan you can see the steps the query takes and which indexes it uses.

Example:
```sql
EXPLAIN SELECT * FROM users WHERE email = 'example@example.com';
```

Sample execution plan output:
```
id | select_type | table | type  | possible_keys  | key      | key_len | ref  | rows | Extra
1  | SIMPLE      | users | index | idx_users_email| email    | 767     | NULL | 10   | Using where
```

Based on the execution plan output, you can optimize as follows:
- **Avoid full table scans**: make sure the query conditions use an index.
- **Reduce the number of returned columns**: query only the columns you need, cutting the amount of data transferred.
- **Optimize join queries**: make sure each subquery in the join runs efficiently.

#### 10.5 Database connection pools and caching

##### 10.5.1 Database connection pools

A database connection pool manages connections effectively, cutting the cost of creating and destroying them and improving concurrent performance.

In Go, you can use the connection-pool features in the `database/sql` package:
```go
package main

import (
    "database/sql"
    "log"
    "time"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    db, err := sql.Open("mysql", "user:password@/dbname")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // set the maximum number of open connections
    db.SetMaxOpenConns(25)

    // set the maximum number of idle connections
    db.SetMaxIdleConns(25)

    // set the maximum lifetime of a connection
    db.SetConnMaxLifetime(5 * time.Minute)
}
```

##### 10.5.2 Caching

A cache sits in front of the database: read requests check the cache first, and the number of database hits drops accordingly. There are two common approaches:

- **In-memory cache**: such as Go's built-in caching, or an LRU cache.
- **Distributed cache**: such as Redis or Memcached.

Example: using Redis for caching
```go
import (
    "context"

    "github.com/redis/go-redis/v9"
)

var ctx = context.Background()
var rdb = redis.NewClient(&redis.Options{
    Addr: "localhost:6379",
    Password: "",
    DB: 0,
})

func setCache(key string, value string) error {
    return rdb.Set(ctx, key, value, 0).Err()
}

func getCache(key string) (string, error) {
    val, err := rdb.Get(ctx, key).Result()
    if err == redis.Nil {
        return "", nil // cache miss
    } else if err != nil {
        return "", err
    }
    return val, nil
}
```

This page records index types and creation, `EXPLAIN` execution-plan analysis, connection-pool parameters, and Redis caching. My habit is to locate the bottleneck with `EXPLAIN` first, then get to work optimizing.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)


## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [ORM](/db/ORM.md)
- [Project](/db/Project.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ORM](/db/ORM.md)
- [Project](/db/Project.md)
