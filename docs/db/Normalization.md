### 3.4 Database Normalization

Database normalization is a set of rules for structuring tables, used to reduce data redundancy and keep the data consistent.

#### 3.4.1 First Normal Form (1NF)
1NF requires that every column in a table holds atomic values that cannot be split further.

**Example:**

Suppose there is a student table recording students' course information. A table that does not satisfy 1NF:

| Student ID | Name     | Courses                     |
|------------|----------|-----------------------------|
| 1          | Zhang San| Math, English               |
| 2          | Li Si    | Physics, Chemistry, Biology |

In the table above, the courses field contains multiple values, which violates 1NF.

**After converting to 1NF:**

| Student ID | Name     | Course    |
|------------|----------|-----------|
| 1          | Zhang San| Math      |
| 1          | Zhang San| English   |
| 2          | Li Si    | Physics   |
| 2          | Li Si    | Chemistry |
| 2          | Li Si    | Biology   |

Now every field holds an indivisible atomic value, so 1NF is satisfied.

#### 3.4.2 Second Normal Form (2NF)
2NF requires that the table satisfies 1NF and that every non-key attribute is fully dependent on the primary key.

**Example:**

Suppose there is an order table recording order information. A table that does not satisfy 2NF:

| Order ID | Customer ID | Customer Name | Product ID | Product Name | Quantity |
|----------|-------------|---------------|------------|--------------|----------|
| 1        | 101         | Zhang San     | P1         | Laptop       | 2        |
| 2        | 102         | Li Si         | P2         | Phone        | 1        |
| 3        | 101         | Zhang San     | P3         | Tablet       | 1        |

In the table above, customer name and product name depend on customer ID and product ID, not on order ID, which violates 2NF.

**After converting to 2NF:**

**Order table:**

| Order ID | Customer ID | Product ID | Quantity |
|----------|-------------|------------|----------|
| 1        | 101         | P1         | 2        |
| 2        | 102         | P2         | 1        |
| 3        | 101         | P3         | 1        |

**Customer table:**

| Customer ID | Customer Name |
|-------------|---------------|
| 101         | Zhang San     |
| 102         | Li Si         |

**Product table:**

| Product ID | Product Name |
|------------|--------------|
| P1         | Laptop       |
| P2         | Phone        |
| P3         | Tablet       |

Now every non-key attribute is fully dependent on the primary key, so 2NF is satisfied.

#### 3.4.3 Third Normal Form (3NF)
3NF requires that the table satisfies 2NF and that no non-key attribute is transitively dependent on the primary key.

**Example:**

Suppose there is an employee table recording employee information. A table that does not satisfy 3NF:

| Employee ID | Name      | Department ID | Department Name |
|-------------|-----------|---------------|-----------------|
| 1           | Zhang San | D1            | Finance         |
| 2           | Li Si     | D2            | HR              |
| 3           | Wang Wu   | D1            | Finance         |

In the table above, department name depends on department ID, and department ID depends on employee ID, which violates 3NF.

**After converting to 3NF:**

**Employee table:**

| Employee ID | Name      | Department ID |
|-------------|-----------|---------------|
| 1           | Zhang San | D1            |
| 2           | Li Si     | D2            |
| 3           | Wang Wu   | D1            |

**Department table:**

| Department ID | Department Name |
|---------------|-----------------|
| D1            | Finance         |
| D2            | HR              |

Now no non-key attribute is transitively dependent on the primary key, so 3NF is satisfied.

#### 3.4.4 BC Normal Form (BCNF)
BCNF is a strengthened version of 3NF; it requires that every key attribute is fully dependent on a candidate key.

**Example:**

Suppose there is a course table recording each course's instructor and time slot. A table that does not satisfy BCNF:

| Course ID | Instructor ID | Time      | Instructor Name |
|-----------|---------------|-----------|-----------------|
| C1        | T1            | Morning   | Zhang San       |
| C2        | T2            | Afternoon | Li Si           |
| C1        | T1            | Afternoon | Zhang San       |

In the table above, instructor name depends on instructor ID, and instructor ID depends on course ID and time, which violates BCNF.

**After converting to BCNF:**

**Course table:**

| Course ID | Instructor ID | Time      |
|-----------|---------------|-----------|
| C1        | T1            | Morning   |
| C2        | T2            | Afternoon |
| C1        | T1            | Afternoon |

**Instructor table:**

| Instructor ID | Instructor Name |
|---------------|-----------------|
| T1            | Zhang San       |
| T2            | Li Si           |

Now every key attribute is fully dependent on a candidate key, so BCNF is satisfied.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)


## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [NoSQL](/db/NoSQL.md)
- [ORM](/db/ORM.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [NoSQL](/db/NoSQL.md)
- [ORM](/db/ORM.md)
