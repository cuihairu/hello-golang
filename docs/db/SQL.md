### Chapter 4: SQL You Must Know

#### 4.1 Basic SQL Syntax

SQL (Structured Query Language) is a standard language for managing and operating relational databases.

##### 4.1.1 The Basic Structure of SQL Statements
An SQL statement typically includes the following parts:

- **SELECT**: used to retrieve data from a database.
- **INSERT**: used to insert data into a database.
- **UPDATE**: used to update data in a database.
- **DELETE**: used to delete data from a database.
- **CREATE**: used to create databases and tables.
- **ALTER**: used to modify databases and tables.
- **DROP**: used to delete databases and tables.

##### 4.1.2 The Components of an SQL Statement
- **SELECT list**: specifies the columns to retrieve.
- **FROM table name**: specifies the table the data comes from.
- **WHERE condition**: specifies the condition used to filter data.
- **GROUP BY list**: groups the data by the specified columns.
- **HAVING condition**: filters the grouped data.
- **ORDER BY list**: sorts the data.

#### 4.2 Data Definition Language (DDL)

Data Definition Language (DDL) is used to define and manage the structures and objects in a database.

##### 4.2.1 CREATE Statements
- **Create a database**:
  ```sql
  CREATE DATABASE mydatabase;
  ```

- **Create a table**:
  ```sql
  CREATE TABLE users (
      id INT PRIMARY KEY,
      name VARCHAR(100),
      age INT
  );
  ```

##### 4.2.2 ALTER Statements
- **Add a new column**:
  ```sql
  ALTER TABLE users ADD COLUMN email VARCHAR(100);
  ```

- **Modify a column type**:
  ```sql
  ALTER TABLE users MODIFY COLUMN age SMALLINT;
  ```

##### 4.2.3 DROP Statements
- **Delete a database**:
  ```sql
  DROP DATABASE mydatabase;
  ```

- **Delete a table**:
  ```sql
  DROP TABLE users;
  ```

#### 4.3 Data Manipulation Language (DML)

Data Manipulation Language (DML) is used to query and modify data.

##### 4.3.1 SELECT Statements
- **Query all columns**:
  ```sql
  SELECT * FROM users;
  ```

- **Query specific columns**:
  ```sql
  SELECT name, age FROM users;
  ```

- **Query with a WHERE condition**:
  ```sql
  SELECT * FROM users WHERE age > 30;
  ```

- **Sort with ORDER BY**:
  ```sql
  SELECT * FROM users ORDER BY age DESC;
  ```

- **Group with GROUP BY**:
  ```sql
  SELECT age, COUNT(*) FROM users GROUP BY age;
  ```

##### 4.3.2 INSERT Statements
- **Insert a new record**:
  ```sql
  INSERT INTO users (name, age) VALUES ('Alice', 25);
  ```

- **Insert multiple records**:
  ```sql
  INSERT INTO users (name, age) VALUES 
  ('Bob', 30), 
  ('Charlie', 35);
  ```

##### 4.3.3 UPDATE Statements
- **Update a record**:
  ```sql
  UPDATE users SET age = 26 WHERE name = 'Alice';
  ```

- **Update multiple records**:
  ```sql
  UPDATE users SET age = age + 1 WHERE age < 30;
  ```

##### 4.3.4 DELETE Statements
- **Delete a record**:
  ```sql
  DELETE FROM users WHERE name = 'Alice';
  ```

- **Delete all records**:
  ```sql
  DELETE FROM users;
  ```

#### 4.4 Data Control Language (DCL)

Data Control Language (DCL) is used to control access permissions on a database.

##### 4.4.1 GRANT Statements
- **Grant permissions to a user**:
  ```sql
  GRANT SELECT, INSERT ON mydatabase.* TO 'username'@'localhost';
  ```

- **Grant all permissions**:
  ```sql
  GRANT ALL PRIVILEGES ON mydatabase.* TO 'username'@'localhost';
  ```

##### 4.4.2 REVOKE Statements
- **Revoke permissions from a user**:
  ```sql
  REVOKE INSERT ON mydatabase.* FROM 'username'@'localhost';
  ```

- **Revoke all permissions**:
  ```sql
  REVOKE ALL PRIVILEGES ON mydatabase.* FROM 'username'@'localhost';
  ```

#### 4.5 Complex Queries (Joins, Subqueries, Set Operations)

##### 4.5.1 Joins (JOIN)
- **Inner join**:
  ```sql
  SELECT users.name, orders.order_id
  FROM users
  INNER JOIN orders ON users.id = orders.user_id;
  ```

- **Left join**:
  ```sql
  SELECT users.name, orders.order_id
  FROM users
  LEFT JOIN orders ON users.id = orders.user_id;
  ```

- **Right join**:
  ```sql
  SELECT users.name, orders.order_id
  FROM users
  RIGHT JOIN orders ON users.id = orders.user_id;
  ```

- **Full join** (supported by some databases; MySQL does not support `FULL JOIN`, but you can simulate it with a `UNION` of a `LEFT JOIN` and a `RIGHT JOIN`):
  ```sql
  SELECT users.name, orders.order_id
  FROM users
  FULL JOIN orders ON users.id = orders.user_id;
  ```

##### 4.5.2 Subqueries
- **Simple subquery**:
  ```sql
  SELECT name FROM users WHERE age > (SELECT AVG(age) FROM users);
  ```

- **Correlated subquery**:
  ```sql
  SELECT name
  FROM users u1
  WHERE age > (SELECT AVG(age) FROM users u2 WHERE u1.id = u2.id);
  ```

##### 4.5.3 Set Operations
- **UNION**:
  ```sql
  SELECT name FROM users
  UNION
  SELECT name FROM customers;
  ```

- **UNION ALL**:
  ```sql
  SELECT name FROM users
  UNION ALL
  SELECT name FROM customers;
  ```

- **INTERSECT** (supported by some databases):
  ```sql
  SELECT name FROM users
  INTERSECT
  SELECT name FROM customers;
  ```

- **EXCEPT** (supported by some databases):
  ```sql
  SELECT name FROM users
  EXCEPT
  SELECT name FROM customers;
  ```

#### 4.6 SQL Optimization Tips

##### 4.6.1 Using Indexes
- **Create an index**:
  ```sql
  CREATE INDEX idx_users_age ON users (age);
  ```

- **Delete an index**:
  ```sql
  DROP INDEX idx_users_age;
  ```

##### 4.6.2 Query Optimization
- **Avoid SELECT *, only query the columns you need**:
  ```sql
  SELECT name, age FROM users;
  ```

- **Use appropriate WHERE conditions to filter data**:
  ```sql
  SELECT name FROM users WHERE age > 30;
  ```

- **Avoid filtering on non-indexed columns**:
  ```sql
  SELECT name FROM users WHERE age > 30;  -- the age column is indexed
  ```

##### 4.6.3 Partitioning and Table Splitting
- **Partitioned table** (MySQL syntax, date boundaries use date string literals directly):
  ```sql
  CREATE TABLE orders (
      order_id INT,
      order_date DATE,
      ...
  )
  PARTITION BY RANGE (order_date) (
      PARTITION p0 VALUES LESS THAN ('2020-01-01'),
      PARTITION p1 VALUES LESS THAN ('2021-01-01')
  );
  ```

##### 4.6.4 Regular Maintenance
- **Analyze tables and indexes**:
  ```sql
  ANALYZE TABLE users;  -- MySQL
  ```

- **Rebuild indexes**:
  ```sql
  REINDEX TABLE users;  -- PostgreSQL (MySQL has no REINDEX; use OPTIMIZE TABLE to rebuild the table)
  ```

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)


## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [Readme](/db/Readme.md)
- [Security](/db/Security.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Readme](/db/Readme.md)
- [Security](/db/Security.md)
