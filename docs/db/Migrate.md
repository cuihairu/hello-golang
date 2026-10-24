### Data Migration and Management

#### 8.1 The Concept of Database Migration

Database migration is the set of operations that keeps data consistent and intact when a database schema changes. Migration tools help developers manage schema changes automatically, including creating, modifying, and dropping table structures, as well as handling data migration and version control.

##### 8.1.1 Benefits of Database Migration
- **Automation**: Reduces the effort and error risk of changing the database structure by hand.
- **Version control**: Tracks changes to the schema, keeping the database structure consistent across environments.
- **Rollback support**: Lets you roll back to a previous version when something goes wrong.

#### 8.2 Database Migration with Goose

Goose is a database migration tool written in Go. It supports multiple databases, including MySQL, PostgreSQL, and SQLite.

##### 8.2.1 Installing Goose
Install Goose with the `go get` command:
```bash
go get -u github.com/pressly/goose/v3/cmd/goose
```

##### 8.2.2 Initializing the Migration Directory
Create a directory in the project to hold migration files:
```bash
mkdir db/migrations
```

##### 8.2.3 Creating a Migration File
Use Goose to create a migration file:
```bash
goose -dir db/migrations create add_users_table sql
```

##### 8.2.4 Writing a Migration Script
In the generated migration file, write SQL to create or modify the database structure. For example, in `db/migrations/20220728120000_add_users_table.sql`:
```sql
-- +goose Up
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

-- +goose Down
DROP TABLE users;
```

##### 8.2.5 Running the Migration
Use Goose to run the database migration:
```bash
goose -dir db/migrations mysql "user:password@tcp(127.0.0.1:3306)/dbname" up
```

##### 8.2.6 Rolling Back a Migration
Use Goose to roll back to the previous version:
```bash
goose -dir db/migrations mysql "user:password@tcp(127.0.0.1:3306)/dbname" down
```

#### 8.3 Database Migration with Flyway

Flyway is another database migration tool, supporting multiple databases and programming languages.

##### 8.3.1 Installing Flyway
Download and extract Flyway:
```bash
curl -L https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/7.10.0/flyway-commandline-7.10.0-linux-x64.tar.gz -o flyway.tar.gz
tar -xzvf flyway.tar.gz
```

##### 8.3.2 Configuring Flyway
Create a config file `flyway.conf` in the Flyway directory:
```ini
flyway.url=jdbc:mysql://localhost:3306/dbname
flyway.user=user
flyway.password=password
flyway.locations=filesystem:sql/migrations
```

##### 8.3.3 Creating the Migration Directory
Create a directory in the project to hold migration files:
```bash
mkdir sql/migrations
```

##### 8.3.4 Writing a Migration Script
Create a migration file in the migration directory, for example `V1__create_users_table.sql`:
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);
```

##### 8.3.5 Running the Migration
Use Flyway to run the database migration:
```bash
flyway -configFiles=flyway.conf migrate
```

##### 8.3.6 Rolling Back a Migration
Flyway does not support rollback directly, but you can achieve a rollback by creating a new migration script. For example, create `V2__drop_users_table.sql`:
```sql
DROP TABLE users;
```

#### 8.4 Database Version Control

Database version control is part of database migration. By managing and recording changes to the database structure, it keeps databases consistent across environments.

##### 8.4.1 The Importance of Version Control
- **Consistency**: Keeps the database structure the same across development, testing, and production environments.
- **Traceability**: Records changes to the database structure, making it easy to trace back and audit.
- **Team collaboration**: Team members can share changes to the database structure, avoiding conflicts and duplicate work.

##### 8.4.2 Version Control in Practice
- **Use a migration tool**: Pick a migration tool that fits (Goose or Flyway, for example) to manage changes to the database structure.
- **Follow version control conventions**: Create a migration script for each change to the database structure, so changes are traceable and reversible.
- **Automated deployment**: Integrate database migration into the automated deployment pipeline, so the database structure updates automatically with every code release.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)


## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [Lib](/db/Lib.md)
- [Mock](/db/Mock.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Lib](/db/Lib.md)
- [Mock](/db/Mock.md)
