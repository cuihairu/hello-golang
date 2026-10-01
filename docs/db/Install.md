### 安装和配置

#### 2.1 安装和配置常用数据库（MySQL、PostgreSQL、SQLite等）

本节将介绍如何在本地环境中安装和配置几种常用的数据库：MySQL、PostgreSQL和SQLite。

##### 2.1.1 安装MySQL

1. **下载和安装**
   - 在[MySQL官网](https://dev.mysql.com/downloads/mysql/)下载适用于您操作系统的安装包。
   - 按照安装向导进行安装。

2. **配置MySQL**
   - 安装完成后，启动MySQL服务。
   - 使用初始root账户登录：
     ```bash
     mysql -u root -p
     ```
   - 配置root账户密码和创建新用户：
     ```sql
     ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
     CREATE USER 'username'@'localhost' IDENTIFIED BY 'user_password';
     GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost' WITH GRANT OPTION;
     ```

3. **测试连接**
   - 使用新用户连接数据库：
     ```bash
     mysql -u username -p
     ```

##### 2.1.2 安装PostgreSQL

1. **下载和安装**
   - 在[PostgreSQL官网](https://www.postgresql.org/download/)下载适用于您操作系统的安装包。
   - 按照安装向导进行安装。

2. **配置PostgreSQL**
   - 安装完成后，初始化数据库并启动PostgreSQL服务。
   - 切换到postgres用户并进入PostgreSQL命令行：
     ```bash
     sudo -i -u postgres
     psql
     ```
   - 配置postgres账户密码和创建新用户：
     ```sql
     ALTER USER postgres PASSWORD 'new_password';
     CREATE USER username WITH PASSWORD 'user_password';
     CREATE DATABASE mydatabase OWNER username;
     ```

3. **测试连接**
   - 使用新用户连接数据库：
     ```bash
     psql -U username -d mydatabase -W
     ```

##### 2.1.3 安装SQLite

1. **下载和安装**
   - 在[SQLite官网](https://www.sqlite.org/download.html)下载适用于您操作系统的安装包。
   - 安装完成后，确保`sqlite3`命令可用。

2. **创建和配置SQLite数据库**
   - 创建一个新的SQLite数据库：
     ```bash
     sqlite3 mydatabase.db
     ```
   - 在SQLite命令行中创建表和插入数据：
     ```sql
     CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER);
     INSERT INTO users (name, age) VALUES ('Alice', 30);
     ```

3. **测试连接**
   - 查询数据库中的数据：
     ```sql
     SELECT * FROM users;
     ```

#### 2.2 配置数据库连接

本节将介绍如何在Go中配置数据库连接，主要使用`database/sql`包，并分别连接MySQL、PostgreSQL和SQLite数据库。

##### 2.2.1 安装依赖包

在Go项目中，首先需要安装相应的数据库驱动程序：

```bash
go get -u github.com/go-sql-driver/mysql
go get -u github.com/lib/pq
go get -u github.com/mattn/go-sqlite3
```

##### 2.2.2 配置MySQL连接

1. **导入包**
   ```go
   import (
       "database/sql"
       _ "github.com/go-sql-driver/mysql"
   )
   ```

2. **建立连接**
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

##### 2.2.3 配置PostgreSQL连接

1. **导入包**
   ```go
   import (
       "database/sql"
       _ "github.com/lib/pq"
   )
   ```

2. **建立连接**
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

##### 2.2.4 配置SQLite连接

1. **导入包**
   ```go
   import (
       "database/sql"
       _ "github.com/mattn/go-sqlite3"
   )
   ```

2. **建立连接**
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

通过上述步骤，您可以成功地在Go中配置并连接到不同的数据库，为后续的数据库操作做好准备。