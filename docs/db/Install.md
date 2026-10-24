### Installation and Configuration

#### 2.1 Installing and Configuring Common Databases (MySQL, PostgreSQL, SQLite, etc.)

This section records how I install and configure a few common databases in a local environment: MySQL, PostgreSQL and SQLite.

##### 2.1.1 Installing MySQL

1. **Download and install**
   - Download the installer for your operating system from the [MySQL official website](https://dev.mysql.com/downloads/mysql/).
   - Follow the installation wizard to install it.

2. **Configure MySQL**
   - After the install finishes, start the MySQL service.
   - Log in with the initial root account:
     ```bash
     mysql -u root -p
     ```
   - Set the root account password and create a new user:
     ```sql
     ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
     CREATE USER 'username'@'localhost' IDENTIFIED BY 'user_password';
     GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost' WITH GRANT OPTION;
     ```

3. **Test the connection**
   - Connect to the database as the new user:
     ```bash
     mysql -u username -p
     ```

##### 2.1.2 Installing PostgreSQL

1. **Download and install**
   - Download the installer for your operating system from the [PostgreSQL official website](https://www.postgresql.org/download/).
   - Follow the installation wizard to install it.

2. **Configure PostgreSQL**
   - After the install finishes, initialize the database and start the PostgreSQL service.
   - Switch to the postgres user and enter the PostgreSQL command line:
     ```bash
     sudo -i -u postgres
     psql
     ```
   - Set the postgres account password and create a new user:
     ```sql
     ALTER USER postgres PASSWORD 'new_password';
     CREATE USER username WITH PASSWORD 'user_password';
     CREATE DATABASE mydatabase OWNER username;
     ```

3. **Test the connection**
   - Connect to the database as the new user:
     ```bash
     psql -U username -d mydatabase -W
     ```

##### 2.1.3 Installing SQLite

1. **Download and install**
   - Download the installer for your operating system from the [SQLite official website](https://www.sqlite.org/download.html).
   - After the install finishes, make sure the `sqlite3` command is available.

2. **Create and configure a SQLite database**
   - Create a new SQLite database:
     ```bash
     sqlite3 mydatabase.db
     ```
   - Create a table and insert data in the SQLite command line:
     ```sql
     CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER);
     INSERT INTO users (name, age) VALUES ('Alice', 30);
     ```

3. **Test the connection**
   - Query the data in the database:
     ```sql
     SELECT * FROM users;
     ```

#### 2.2 Configuring Database Connections

This section records how I configure database connections in Go. I mainly use the `database/sql` package, and connect to MySQL, PostgreSQL and SQLite databases separately.

##### 2.2.1 Installing the Dependency Packages

First install the database drivers in the Go project:

```bash
go get -u github.com/go-sql-driver/mysql
go get -u github.com/lib/pq
go get -u github.com/mattn/go-sqlite3
```

##### 2.2.2 Configuring a MySQL Connection

1. **Import the package**
   ```go
   import (
       "database/sql"
       _ "github.com/go-sql-driver/mysql"
   )
   ```

2. **Establish the connection**
   ```go
   func connectMySQL() (*sql.DB, error) {
       dsn := "username:user_password@tcp(127.0.0.1:3306)/mydatabase"
       db, err := sql.Open("mysql", dsn)
       if err != nil {
           return nil, err
       }
       if err := db.Ping(); err != nil {
           return nil, err
       }
       return db, nil
   }
   ```

##### 2.2.3 Configuring a PostgreSQL Connection

1. **Import the package**
   ```go
   import (
       "database/sql"
       _ "github.com/lib/pq"
   )
   ```

2. **Establish the connection**
   ```go
   func connectPostgres() (*sql.DB, error) {
       dsn := "user=username password=user_password dbname=mydatabase sslmode=disable"
       db, err := sql.Open("postgres", dsn)
       if err != nil {
           return nil, err
       }
       if err := db.Ping(); err != nil {
           return nil, err
       }
       return db, nil
   }
   ```

##### 2.2.4 Configuring a SQLite Connection

1. **Import the package**
   ```go
   import (
       "database/sql"
       _ "github.com/mattn/go-sqlite3"
   )
   ```

2. **Establish the connection**
   ```go
   func connectSQLite() (*sql.DB, error) {
       db, err := sql.Open("sqlite3", "mydatabase.db")
       if err != nil {
           return nil, err
       }
       if err := db.Ping(); err != nil {
           return nil, err
       }
       return db, nil
   }
   ```

That gets the connections for all three databases set up. The CRUD operations that follow go through the corresponding `*sql.DB`.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)


## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [GraphQL](/db/GraphQL.md)
- [Lib](/db/Lib.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Lib](/db/Lib.md)
