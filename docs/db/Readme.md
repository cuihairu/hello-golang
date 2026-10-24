### Databases and Persistence

#### 1.1 What is a database
A database is an organized collection of data, used to store data, modify data, and retrieve data by condition. A database system (DBMS) provides a unified interface for these operations: insert, delete, update, and query all go through the same route.

##### 1.1.1 Basic concepts of a database
- **Data**: raw facts and figures, which can be text, images, sound, and so on.
- **Database Management System (DBMS)**: software used to create, manage, and operate databases, such as MySQL, PostgreSQL, and SQLite.
- **Table**: the structured way to store data in a database, made up of rows and columns.
- **Record**: a row in a table, representing one specific data item.
- **Field**: a column in a table, representing one attribute of a data item.

##### 1.1.2 Functions of a database
- **Data storage**: keep the data stored, without losing it or getting it wrong.
- **Data retrieval**: find the data by condition.
- **Data management**: organize and maintain the data.
- **Data security**: block unauthorized access and tampering.

#### 1.2 Types of databases
Databases can be divided into different types by structure and function. The common ones are:

##### 1.2.1 Relational databases
- A data management system based on the relational model, where data is stored in tables.
- Examples: MySQL, PostgreSQL, SQLite, Oracle.

##### 1.2.2 Non-relational databases (NoSQL)
- Mainly used for large-scale data and high-concurrency applications, with diverse storage approaches.
- Examples: MongoDB (document), Redis (key-value), Cassandra (column-store), Neo4j (graph database).

##### 1.2.3 In-memory databases
- Data is stored mainly in memory, so reads and writes are fast; often used as a cache.
- Examples: Redis, Memcached.

##### 1.2.4 Distributed databases
- Data is spread across multiple nodes, to provide high availability and scalability.
- Examples: CockroachDB, Cassandra.

#### 1.3 Advantages of Go for database programming
Go suits database programming: it compiles to machine code and runs efficiently, it has built-in concurrency support, and the standard library `database/sql` provides a unified interface for database operations.

##### 1.3.1 High performance
- Go compiles to machine code and runs efficiently.
- Built-in concurrency support suits high-concurrency database operations.

##### 1.3.2 Concise and easy to use
- The syntax is concise and easy to pick up.
- A strong type system cuts down on runtime errors.

##### 1.3.3 Rich standard library
- The `database/sql` package provides a unified interface for database operations.
- Rich third-party library support, such as GORM and Ent.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)


## Sibling pages

- [Availability](/zh/db/Availability.md)
- [Base](/zh/db/Base.md)
- [ConnectPool](/zh/db/ConnectPool.md)
- [Project](/zh/db/Project.md)
- [SQL](/zh/db/SQL.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Project](/zh/db/Project.md)
- [SQL](/zh/db/SQL.md)
