### 第3章 数据库基础

#### 3.1 数据库基础概念

本节将介绍数据库的基本概念和术语，帮助读者理解数据库的基本结构和功能。

##### 3.1.1 数据库
- **定义**：数据库是一种有组织的数据集合，用于高效地存储、管理和检索数据。
- **作用**：通过数据库管理系统（DBMS），用户可以方便地进行数据操作和管理。

##### 3.1.2 表
- **定义**：表是数据库中用于存储数据的基本单位，由行和列组成。
- **组成**：每个表有多个字段（列），每个字段有特定的数据类型；表中的每一行称为记录。

##### 3.1.3 记录和字段
- **记录**：表中的一行，表示一条具体的数据项。
- **字段**：表中的一列，表示数据项的一个属性。

##### 3.1.4 主键
- **定义**：主键是表中的一个或多个字段，其值可以唯一标识表中的每一条记录。
- **作用**：确保数据的唯一性和完整性。

##### 3.1.5 外键
- **定义**：外键是一个表中的字段，用于建立与另一个表中主键的连接关系。
- **作用**：确保数据的参照完整性。

##### 3.1.6 索引
- **定义**：索引是数据库中的一种结构，用于加速数据的检索。
- **作用**：提高查询效率，但会增加数据写入的时间和存储空间。

#### 3.2 SQL语言简介

SQL（Structured Query Language，结构化查询语言）是用于管理和操作关系型数据库的标准语言。

##### 3.2.1 SQL的基本语法
- **数据定义语言（DDL）**：用于定义和管理数据库结构。
  - CREATE：创建数据库、表、视图等。
  - ALTER：修改数据库、表结构。
  - DROP：删除数据库、表、视图等。

- **数据操作语言（DML）**：用于查询和修改数据。
  - SELECT：查询数据。
  - INSERT：插入数据。
  - UPDATE：更新数据。
  - DELETE：删除数据。

- **数据控制语言（DCL）**：用于控制访问权限。
  - GRANT：授予权限。
  - REVOKE：撤销权限。

##### 3.2.2 常用SQL操作
- **查询数据**
  ```sql
  SELECT * FROM users WHERE age > 30;
  ```

- **插入数据**
  ```sql
  INSERT INTO users (name, age) VALUES ('Bob', 25);
  ```

- **更新数据**
  ```sql
  UPDATE users SET age = 26 WHERE name = 'Bob';
  ```

- **删除数据**
  ```sql
  DELETE FROM users WHERE name = 'Bob';
  ```

#### 3.3 数据库设计原则

良好的数据库设计可以提高数据的存储效率和操作性能。以下是一些基本的数据库设计原则：

##### 3.3.1 实体-关系模型（ER模型）
- **定义**：实体-关系模型是一种用于描述数据库结构的模型，通过实体和关系来表示数据。
- **作用**：帮助设计者直观地理解和设计数据库。

##### 3.3.2 数据库规范化
- **定义**：规范化是将数据组织成无冗余、依赖明确的表的过程。
- **作用**：减少数据冗余，提高数据一致性。

##### 3.3.3 数据完整性
- **定义**：数据完整性是确保数据库中数据的准确性和一致性。
- **种类**：
  - 实体完整性：每个表必须有一个主键，且主键值唯一。
  - 参照完整性：外键值必须引用主键值，确保关系的有效性。
  - 域完整性：字段值必须符合预定义的规则或范围。

##### 3.3.4 数据库性能优化
- **定义**：性能优化是提高数据库查询和操作效率的方法。
- **方法**：
  - 使用索引加速查询。
  - 合理设计表结构和关系。
  - 避免过多的嵌套查询。

#### 3.4 数据库范式

数据库范式是数据库设计中用于规范化数据结构的一系列规则，目的是减少数据冗余，提高数据一致性。

##### 3.4.1 第一范式（1NF）
- **定义**：确保每列的值都是不可分割的原子值。
- **示例**：一个表中每个字段只能包含单一值，而不能包含集合、数组等。

##### 3.4.2 第二范式（2NF）
- **定义**：满足1NF，并且表中的每个非主属性完全依赖于主键。
- **示例**：消除部分依赖，将相关数据分拆到不同的表中。

##### 3.4.3 第三范式（3NF）
- **定义**：满足2NF，并且每个非主属性不传递依赖于主键。
- **示例**：消除传递依赖，将相关数据进一步分拆。

##### 3.4.4 BC范式（BCNF）
- **定义**：满足3NF，并且每个主属性都完全依赖于候选键。
- **示例**：确保所有主属性的依赖关系都是通过候选键直接建立的。
