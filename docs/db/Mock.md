### 测试

#### 11.1 数据库测试的重要性

数据库操作出错，轻则数据不一致，重则丢数据。测数据库，就是把这些问题挡在生产环境之前。测试目标有几类：

- 数据操作的正确性：插入、更新、删除后数据是预期的值。
- 数据完整性：外键约束、唯一性约束等规则生效。
- 性能：数据库操作在预期时间内完成。
- 业务逻辑：落在数据库里的业务规则执行正确。

#### 11.2 使用mock库进行数据库测试

在单元测试中，使用 mock 库可以模拟数据库操作，避免对实际数据库的依赖，从而提高测试的独立性和速度。Go 语言中常用的 mock 库包括 `go-sqlmock`。

##### 示例：使用 `go-sqlmock` 进行数据库测试

1. 安装 `go-sqlmock`：
```bash
go get github.com/DATA-DOG/go-sqlmock
```

2. 编写测试代码：
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

#### 11.3 编写高效的数据库测试用例

编写高效的数据库测试用例需要遵循以下原则：

- **独立性**：每个测试用例应独立运行，避免相互依赖。
- **重置环境**：在测试开始前重置数据库状态，确保测试环境的一致性。
- **最小化依赖**：尽量减少对外部依赖的需求，例如使用 mock 数据库。
- **覆盖全面**：编写覆盖所有主要功能和边界情况的测试用例。

##### 示例：编写高效的数据库测试用例

1. 创建测试数据库并重置状态：
```go
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

2. 编写测试用例：
```go
func TestInsertUser(t *testing.T) {
    db := setupTestDB(t)
    defer db.Close()

    user := &User{Name: "Bob", Email: "bob@example.com"}
    err := InsertUser(db, user)
    if err != nil {
        t.Fatalf("failed to insert user: %s", err)
    }

    // 验证插入的用户是否存在
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

#### 11.4 数据库集成测试

集成测试在真实的数据库环境中运行，验证整个系统的数据库操作的正确性和性能。集成测试通常包括以下步骤：

- **准备测试数据**：在测试开始前插入必要的测试数据。
- **执行测试操作**：调用实际的数据库操作代码。
- **验证结果**：检查数据库中的数据是否符合预期。

##### 示例：编写数据库集成测试

1. 准备测试数据：
```go
func prepareTestData(db *sql.DB) error {
    _, err := db.Exec("INSERT INTO users (name, email) VALUES (?, ?)", "Charlie", "charlie@example.com")
    return err
}
```

2. 执行集成测试：
```go
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

单元测试用 `go-sqlmock` 隔离数据库，跑得快、不依赖环境；集成测试连真实数据库，验证建表、约束和 SQL 语句本身。两类测试配合使用。