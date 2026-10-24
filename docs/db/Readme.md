### Databases and Persistence

#### 1.1 What is a Database
A database is a collection of organized data, used to store data, change data, and find data back by condition. A database system (DBMS) provides a unified interface for these operations; inserts, deletes, updates and queries all go through the same mechanism.

##### 1.1.1 Basic Concepts of a Database
- **Data**: raw facts and numbers, which can be text, images, sound, etc.
- **Database Management System (DBMS)**: a kind of software used to create, manage and operate a database, such as MySQL, PostgreSQL, SQLite, etc.
- **Table**: a structured way of storing data in a database, composed of rows and columns.
- **Record**: a single row in a table, representing one concrete data item.
- **Field**: a single column in a table, representing one attribute of a data item.

##### 1.1.2 Functions of a Database
- **Data storage**: keep the data stored, without loss or corruption.
- **Data retrieval**: find data back by condition.
- **Data management**: organize and maintain the data.
- **Data security**: block unauthorized access and tampering.

#### 1.2 Types of Databases
Databases fall into different types by their structure and function. Common types are:

##### 1.2.1 Relational Databases
- A database management system based on the relational model; data is stored in table form.
- Examples: MySQL, PostgreSQL, SQLite, Oracle.

##### 1.2.2 Non-relational Databases (NoSQL)
- Mainly used to handle large-scale data and high-concurrency applications, with varied storage formats.
- Examples: MongoDB (document), Redis (key-value), Cassandra (columnar), Neo4j (graph).

##### 1.2.3 In-memory Databases
- Data is stored primarily in memory; reads and writes are fast, often used as a cache.
- Examples: Redis, Memcached.

##### 1.2.4 Distributed Databases
- Data is spread across multiple nodes, to provide high availability and scalability.
- Examples: CockroachDB, Cassandra.

#### 1.3 Advantages of Go for Database Programming
Go is well suited to database programming: it compiles to machine code for high execution efficiency, has built-in concurrency support, and the standard library `database/sql` gives a unified interface for database operations.

##### 1.3.1 High Performance
- Go compiles to machine code, so execution is efficient.
- Built-in concurrency support makes it suitable for high-concurrency database operations.

##### 1.3.2 Concise and Easy to Use
- Concise syntax, easy to get started with.
- Strong type system reduces runtime errors.

##### 1.3.3 Rich Standard Library
- The `database/sql` package provides a unified interface for database operations.
- Rich third-party library support, such as GORM and Ent.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)


## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [Project](/db/Project.md)
- [SQL](/db/SQL.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Project](/db/Project.md)
- [SQL](/db/SQL.md)
