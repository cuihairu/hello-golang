### Chapter 3: Database Fundamentals

#### 3.1 Basic Concepts of Databases

This section pins down a few terms that will come up again and again later: database, table, record, field, primary key, foreign key, index.

##### 3.1.1 Database
- **Definition**: a database is a collection of organized data, used to store, manage and retrieve data efficiently.
- **Purpose**: through a database management system (DBMS), users can conveniently carry out data operations and management.

##### 3.1.2 Table
- **Definition**: a table is the basic unit for storing data in a database, composed of rows and columns.
- **Composition**: each table has multiple fields (columns), and each field has a specific data type; each row in the table is called a record.

##### 3.1.3 Record and Field
- **Record**: a row in a table, representing one concrete data item.
- **Field**: a column in a table, representing one attribute of a data item.

##### 3.1.4 Primary Key
A primary key is one or more fields in a table. The primary key value of every record is unique, and it is what identifies a record uniquely.

##### 3.1.5 Foreign Key
A foreign key is a field in one table that points to the primary key of another table, so every record in the child table can find its match in the parent table.

##### 3.1.6 Index
An index is a structure built to speed up retrieval. Lookups get faster, but writes have to maintain an extra copy and storage takes up more room.

#### 3.2 Introduction to the SQL Language

SQL (Structured Query Language) is the standard language for managing and operating relational databases.

##### 3.2.1 Basic SQL Syntax
- **Data Definition Language (DDL)**: used to define and manage database structure.
  - CREATE: create databases, tables, views, etc.
  - ALTER: modify databases and table structure.
  - DROP: delete databases, tables, views, etc.

- **Data Manipulation Language (DML)**: used to query and modify data.
  - SELECT: query data.
  - INSERT: insert data.
  - UPDATE: update data.
  - DELETE: delete data.

- **Data Control Language (DCL)**: used to control access permissions.
  - GRANT: grant permissions.
  - REVOKE: revoke permissions.

##### 3.2.2 Common SQL Operations
- **Query data**
  ```sql
  SELECT * FROM users WHERE age > 30;
  ```

- **Insert data**
  ```sql
  INSERT INTO users (name, age) VALUES ('Bob', 25);
  ```

- **Update data**
  ```sql
  UPDATE users SET age = 26 WHERE name = 'Bob';
  ```

- **Delete data**
  ```sql
  DELETE FROM users WHERE name = 'Bob';
  ```

#### 3.3 Database Design Principles

There are four principles in database design, covering respectively how the structure is described, how the data is laid out, how constraints are set, and how queries are sped up:

##### 3.3.1 Entity-Relationship Model (ER Model)
The ER model describes database structure in terms of entities and relationships. When designing, first use it to think through the relationships between tables, then start creating them.

##### 3.3.2 Database Normalization
Normalization splits the data into tables with little redundancy and clear dependency relationships. The same piece of data is stored in only one place, so a change cannot leave several places inconsistent with each other.

##### 3.3.3 Data Integrity
- **Definition**: data integrity ensures the accuracy and consistency of the data in a database.
- **Kinds**:
  - Entity integrity: every table must have a primary key, and primary key values must be unique.
  - Referential integrity: foreign key values must reference primary key values, ensuring the validity of the relationship.
  - Domain integrity: field values must conform to predefined rules or ranges.

##### 3.3.4 Database Performance Optimization
- **Definition**: performance optimization is about improving the efficiency of database queries and operations.
- **Methods**:
  - Use indexes to speed up queries.
  - Design table structure and relationships sensibly.
  - Avoid excessive nested queries.

#### 3.4 Database Normal Forms

Database normal forms are a series of rules used in database design to normalize the data structure. The goal is to reduce data redundancy and improve data consistency.

##### 3.4.1 First Normal Form (1NF)
- **Definition**: ensure every column value is an indivisible atomic value.
- **Example**: in a table, every field can only hold a single value, not collections or arrays.

##### 3.4.2 Second Normal Form (2NF)
- **Definition**: satisfies 1NF, and every non-prime attribute in the table fully depends on the primary key.
- **Example**: eliminate partial dependencies by splitting the related data out into different tables.

##### 3.4.3 Third Normal Form (3NF)
- **Definition**: satisfies 2NF, and no non-prime attribute transitively depends on the primary key.
- **Example**: eliminate transitive dependencies by splitting the related data further.

##### 3.4.4 BC Normal Form (BCNF)
- **Definition**: satisfies 3NF, and every prime attribute fully depends on a candidate key.
- **Example**: ensure that every prime attribute's dependency is established directly through a candidate key.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)

## Sibling pages

- [Availability](/db/Availability.md)
- [ConnectPool](/db/ConnectPool.md)
- [GraphQL](/db/GraphQL.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Availability](/db/Availability.md)
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
