### 第4章 必知必会SQL

#### 4.1 SQL基础语法

SQL（Structured Query Language，结构化查询语言）是一种用于管理和操作关系型数据库的标准语言。

##### 4.1.1 SQL语句的基本结构
SQL 语句通常包括以下部分：

- **SELECT**：用于从数据库中检索数据。
- **INSERT**：用于向数据库中插入数据。
- **UPDATE**：用于更新数据库中的数据。
- **DELETE**：用于从数据库中删除数据。
- **CREATE**：用于创建数据库和表。
- **ALTER**：用于修改数据库和表。
- **DROP**：用于删除数据库和表。

##### 4.1.2 SQL语句的组成部分
- **SELECT 列表**：指定要检索的列。
- **FROM 表名**：指定数据来源的表。
- **WHERE 条件**：指定筛选数据的条件。
- **GROUP BY 列表**：按指定列对数据进行分组。
- **HAVING 条件**：对分组后的数据进行过滤。
- **ORDER BY 列表**：对数据进行排序。

#### 4.2 数据定义语言（DDL）

数据定义语言（DDL）用于定义和管理数据库中的结构和对象。

##### 4.2.1 CREATE 语句
- **创建数据库**：
  ```sql
  CREATE DATABASE mydatabase;
  ```

- **创建表**：
  ```sql
  CREATE TABLE users (
      id INT PRIMARY KEY,
      name VARCHAR(100),
      age INT
  );
  ```

##### 4.2.2 ALTER 语句
- **添加新列**：
  ```sql
  ALTER TABLE users ADD COLUMN email VARCHAR(100);
  ```

- **修改列类型**：
  ```sql
  ALTER TABLE users MODIFY COLUMN age SMALLINT;
  ```

##### 4.2.3 DROP 语句
- **删除数据库**：
  ```sql
  DROP DATABASE mydatabase;
  ```

- **删除表**：
  ```sql
  DROP TABLE users;
  ```

#### 4.3 数据操作语言（DML）

数据操作语言（DML）用于查询和修改数据。

##### 4.3.1 SELECT 语句
- **查询所有列**：
  ```sql
  SELECT * FROM users;
  ```

- **查询指定列**：
  ```sql
  SELECT name, age FROM users;
  ```

- **使用 WHERE 条件查询**：
  ```sql
  SELECT * FROM users WHERE age > 30;
  ```

- **使用 ORDER BY 排序**：
  ```sql
  SELECT * FROM users ORDER BY age DESC;
  ```

- **使用 GROUP BY 分组**：
  ```sql
  SELECT age, COUNT(*) FROM users GROUP BY age;
  ```

##### 4.3.2 INSERT 语句
- **插入新记录**：
  ```sql
  INSERT INTO users (name, age) VALUES ('Alice', 25);
  ```

- **插入多条记录**：
  ```sql
  INSERT INTO users (name, age) VALUES 
  ('Bob', 30), 
  ('Charlie', 35);
  ```

##### 4.3.3 UPDATE 语句
- **更新记录**：
  ```sql
  UPDATE users SET age = 26 WHERE name = 'Alice';
  ```

- **更新多条记录**：
  ```sql
  UPDATE users SET age = age + 1 WHERE age < 30;
  ```

##### 4.3.4 DELETE 语句
- **删除记录**：
  ```sql
  DELETE FROM users WHERE name = 'Alice';
  ```

- **删除所有记录**：
  ```sql
  DELETE FROM users;
  ```

#### 4.4 数据控制语言（DCL）

数据控制语言（DCL）用于控制数据库的访问权限。

##### 4.4.1 GRANT 语句
- **授予用户权限**：
  ```sql
  GRANT SELECT, INSERT ON mydatabase.* TO 'username'@'localhost';
  ```

- **授予所有权限**：
  ```sql
  GRANT ALL PRIVILEGES ON mydatabase.* TO 'username'@'localhost';
  ```

##### 4.4.2 REVOKE 语句
- **撤销用户权限**：
  ```sql
  REVOKE INSERT ON mydatabase.* FROM 'username'@'localhost';
  ```

- **撤销所有权限**：
  ```sql
  REVOKE ALL PRIVILEGES ON mydatabase.* FROM 'username'@'localhost';
  ```

#### 4.5 复杂查询（连接、子查询、集合操作）

复杂查询包括表的连接、子查询以及集合操作。

##### 4.5.1 连接（JOIN）
- **内连接**：
  ```sql
  SELECT users.name, orders.order_id
  FROM users
  INNER JOIN orders ON users.id = orders.user_id;
  ```

- **左连接**：
  ```sql
  SELECT users.name, orders.order_id
  FROM users
  LEFT JOIN orders ON users.id = orders.user_id;
  ```

- **右连接**：
  ```sql
  SELECT users.name, orders.order_id
  FROM users
  RIGHT JOIN orders ON users.id = orders.user_id;
  ```

- **全连接**：
  ```sql
  SELECT users.name, orders.order_id
  FROM users
  FULL JOIN orders ON users.id = orders.user_id;
  ```

##### 4.5.2 子查询
- **简单子查询**：
  ```sql
  SELECT name FROM users WHERE age > (SELECT AVG(age) FROM users);
  ```

- **相关子查询**：
  ```sql
  SELECT name
  FROM users u1
  WHERE age > (SELECT AVG(age) FROM users u2 WHERE u1.id = u2.id);
  ```

##### 4.5.3 集合操作
- **UNION**：
  ```sql
  SELECT name FROM users
  UNION
  SELECT name FROM customers;
  ```

- **UNION ALL**：
  ```sql
  SELECT name FROM users
  UNION ALL
  SELECT name FROM customers;
  ```

- **INTERSECT**（某些数据库支持）：
  ```sql
  SELECT name FROM users
  INTERSECT
  SELECT name FROM customers;
  ```

- **EXCEPT**（某些数据库支持）：
  ```sql
  SELECT name FROM users
  EXCEPT
  SELECT name FROM customers;
  ```

#### 4.6 SQL优化技巧

SQL优化技巧帮助提高查询和操作的性能。

##### 4.6.1 使用索引
- **创建索引**：
  ```sql
  CREATE INDEX idx_users_age ON users (age);
  ```

- **删除索引**：
  ```sql
  DROP INDEX idx_users_age;
  ```

##### 4.6.2 查询优化
- **避免 SELECT *，只查询需要的列**：
  ```sql
  SELECT name, age FROM users;
  ```

- **使用适当的 WHERE 条件过滤数据**：
  ```sql
  SELECT name FROM users WHERE age > 30;
  ```

- **避免使用非索引列进行过滤**：
  ```sql
  SELECT name FROM users WHERE age > 30;  -- age 列已建立索引
  ```

##### 4.6.3 分区和分表
- **分区表**：
  ```sql
  CREATE TABLE orders (
      order_id INT,
      order_date DATE,
      ...
  )
  PARTITION BY RANGE (order_date) (
      PARTITION p0 VALUES LESS THAN (TO_DATE('2020-01-01')),
      PARTITION p1 VALUES LESS THAN (TO_DATE('2021-01-01'))
  );
  ```

##### 4.6.4 定期维护
- **分析表和索引**：
  ```sql
  ANALYZE TABLE users;
  ```

- **重建索引**：
  ```sql
  REINDEX TABLE users;
  ```

通过掌握这些SQL基础语法、数据定义语言（DDL）、数据操作语言（DML）、数据控制语言（DCL）、复杂查询和SQL优化技巧，读者可以高效地管理和操作数据库。