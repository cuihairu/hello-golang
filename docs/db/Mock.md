### Testing

#### 11.1 Why database testing matters

When database operations go wrong, the result ranges from inconsistent data all the way to lost data. Testing the database is what stops those problems from ever reaching production. There are several categories of test goals:

- Correctness of data operations: after inserting, updating, and deleting, the data holds the expected values.
- Data integrity: rules such as foreign-key constraints and uniqueness constraints actually take effect.
- Performance: database operations complete within the expected time.
- Business logic: the business rules that live in the database execute correctly.

#### 11.2 Testing databases with mock libraries

In unit tests, mock libraries let you simulate database operations without depending on a real database, which makes tests more independent and faster. A commonly used mock library in Go is `go-sqlmock`.

##### Example: testing a database with `go-sqlmock`

1. Install `go-sqlmock`:
```bash
go get github.com/DATA-DOG/go-sqlmock
```

2. Write the test code:
```go
package main

import (
    "database/sql"
    "testing"

    "github.com/DATA-DOG/go-sqlmock"
    _ "github.com/go-sql-driver/mysql"
)

func TestGetUserByID(t *testing.T) {
    db, mock, err := sqlmock.New()
    if err != nil {
        t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
    }
    defer db.Close()

    rows := sqlmock.NewRows([]string{"id", "name", "email"}).
        AddRow(1, "Alice", "alice@example.com")

    mock.ExpectQuery("SELECT id, name, email FROM users WHERE id = ?").
        WithArgs(1).
        WillReturnRows(rows)

    user, err := GetUserByID(db, 1)
    if err != nil {
        t.Errorf("unexpected error: %s", err)
    }

    if user.Name != "Alice" {
        t.Errorf("expected name to be Alice, got %s", user.Name)
    }
}

func GetUserByID(db *sql.DB, id int) (*User, error) {
    row := db.QueryRow("SELECT id, name, email FROM users WHERE id = ?", id)
    user := new(User)
    err := row.Scan(&user.ID, &user.Name, &user.Email)
    if err != nil {
        return nil, err
    }
    return user, nil
}

type User struct {
    ID    int
    Name  string
    Email string
}
```

#### 11.3 Writing efficient database test cases

Writing efficient database test cases calls for the following principles:

- **Independence**: each test case should run on its own, without depending on others.
- **Reset the environment**: reset the database state before the test starts, so the test environment is consistent.
- **Minimize dependencies**: reduce reliance on external dependencies as much as possible, for example by using a mock database.
- **Broad coverage**: write test cases that cover all the main functionality and the edge cases.

##### Example: writing efficient database test cases

1. Create a test database and reset its state:
```go
import (
    "database/sql"
    "testing"
)

func setupTestDB(t *testing.T) *sql.DB {
    db, err := sql.Open("mysql", "user:password@tcp(localhost:3306)/testdb")
    if err != nil {
        t.Fatalf("failed to connect to test database: %s", err)
    }

    _, err = db.Exec("TRUNCATE TABLE users")
    if err != nil {
        t.Fatalf("failed to reset test database: %s", err)
    }

    return db
}
```

2. Write the test cases:
```go
import (
    "database/sql"
    "testing"
)

func InsertUser(db *sql.DB, user *User) error {
    result, err := db.Exec("INSERT INTO users (name, email) VALUES (?, ?)", user.Name, user.Email)
    if err != nil {
        return err
    }
    if id, err := result.LastInsertId(); err == nil {
        user.ID = int(id)
    }
    return nil
}

func TestInsertUser(t *testing.T) {
    db := setupTestDB(t)
    defer db.Close()

    user := &User{Name: "Bob", Email: "bob@example.com"}
    err := InsertUser(db, user)
    if err != nil {
        t.Fatalf("failed to insert user: %s", err)
    }

    // check whether the inserted user exists
    row := db.QueryRow("SELECT id, name, email FROM users WHERE email = ?", "bob@example.com")
    err = row.Scan(&user.ID, &user.Name, &user.Email)
    if err != nil {
        t.Fatalf("failed to retrieve inserted user: %s", err)
    }

    if user.Name != "Bob" {
        t.Errorf("expected name to be Bob, got %s", user.Name)
    }
}
```

#### 11.4 Database integration tests

Integration tests run against a real database environment and verify the correctness and performance of the system's database operations. An integration test usually has the following steps:

- **Prepare test data**: insert the required test data before the test starts.
- **Run the operations under test**: call the actual database operation code.
- **Verify the results**: check that the data in the database matches expectations.

##### Example: writing a database integration test

1. Prepare the test data:
```go
func prepareTestData(db *sql.DB) error {
    _, err := db.Exec("INSERT INTO users (name, email) VALUES (?, ?)", "Charlie", "charlie@example.com")
    return err
}
```

2. Run the integration test:
```go
import (
    "database/sql"
    "testing"
)

func UpdateUser(db *sql.DB, user *User) error {
    _, err := db.Exec("UPDATE users SET name = ?, email = ? WHERE id = ?", user.Name, user.Email, user.ID)
    return err
}

func TestUpdateUser(t *testing.T) {
    db := setupTestDB(t)
    defer db.Close()

    err := prepareTestData(db)
    if err != nil {
        t.Fatalf("failed to prepare test data: %s", err)
    }

    user := &User{ID: 1, Name: "Charlie", Email: "charlie_updated@example.com"}
    err = UpdateUser(db, user)
    if err != nil {
        t.Fatalf("failed to update user: %s", err)
    }

    row := db.QueryRow("SELECT id, name, email FROM users WHERE id = ?", 1)
    err = row.Scan(&user.ID, &user.Name, &user.Email)
    if err != nil {
        t.Fatalf("failed to retrieve updated user: %s", err)
    }

    if user.Email != "charlie_updated@example.com" {
        t.Errorf("expected email to be charlie_updated@example.com, got %s", user.Email)
    }
}
```

Use `go-sqlmock` in unit tests to isolate the database — they run fast and depend on no environment. Integration tests connect to a real database to verify table creation, constraints, and the SQL statements themselves. Use the two kinds of test together.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)
- [go-sqlmock](https://github.com/DATA-DOG/go-sqlmock)


## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [Migrate](/db/Migrate.md)
- [Monitor](/db/Monitor.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Migrate](/db/Migrate.md)
- [Monitor](/db/Monitor.md)
