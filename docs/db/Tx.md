###  Transaction Handling

#### 9.1 The Concept of Transactions

A transaction is a group of database operations treated as a single unit of work: either all succeed, or all roll back. This keeps data consistent and intact. Transactions have four important properties, called the ACID properties:

- **Atomicity**: All operations in a transaction either all succeed or all fail; there is no partial success.
- **Consistency**: The database must be in a consistent state both before and after a transaction.
- **Isolation**: When several transactions run concurrently, they do not interfere with one another.
- **Durability**: Once a transaction is committed, its changes to the database are permanent; even a system failure does not lose them.

#### 9.2 Transaction Management with `database/sql`

In Go, a `database/sql` transaction means getting a `tx` from `db.Begin()`, running statements on that `tx`, calling `Rollback()` on error, and `Commit()` when things go right:

##### 9.2.1 Starting a Transaction
Use the `db.Begin` method to start a transaction:
```go
tx, err := db.Begin()
if err != nil {
    log.Fatal(err)
}
```

##### 9.2.2 Executing Transaction Operations
Run SQL operations inside the transaction:
```go
_, err = tx.Exec("INSERT INTO users (name, email) VALUES (?, ?)", "Alice", "alice@example.com")
if err != nil {
    tx.Rollback() // roll back the transaction on error
    log.Fatal(err)
}
```

##### 9.2.3 Committing or Rolling Back a Transaction
Commit the transaction:
```go
err = tx.Commit()
if err != nil {
    tx.Rollback() // roll back if the commit fails
    log.Fatal(err)
}
```

Roll back the transaction:
```go
err = tx.Rollback()
if err != nil {
    log.Fatal(err)
}
```

Full example:
```go
tx, err := db.Begin()
if err != nil {
    log.Fatal(err)
}

_, err = tx.Exec("INSERT INTO users (name, email) VALUES (?, ?)", "Alice", "alice@example.com")
if err != nil {
    tx.Rollback()
    log.Fatal(err)
}

_, err = tx.Exec("INSERT INTO accounts (user_id, balance) VALUES (?, ?)", 1, 1000)
if err != nil {
    tx.Rollback()
    log.Fatal(err)
}

err = tx.Commit()
if err != nil {
    tx.Rollback()
    log.Fatal(err)
}
```

#### 9.3 Transaction Management in ORM Frameworks

Different ORM frameworks offer different ways to manage transactions.

##### 9.3.1 Transaction Management in GORM
In GORM, use the `Transaction` method:
```go
db.Transaction(func(tx *gorm.DB) error {
    if err := tx.Create(&User{Name: "Alice", Email: "alice@example.com"}).Error; err != nil {
        return err // return the error; the transaction rolls back automatically
    }

    if err := tx.Create(&Account{UserID: 1, Balance: 1000}).Error; err != nil {
        return err
    }

    return nil // return nil; the transaction commits automatically
})
```

##### 9.3.2 Transaction Management in Ent
In Ent, use the `Tx` method:
```go
tx, err := client.Tx(ctx)
if err != nil {
    log.Fatal(err)
}

_, err = tx.User.Create().SetName("Alice").SetEmail("alice@example.com").Save(ctx)
if err != nil {
    tx.Rollback()
    log.Fatal(err)
}

_, err = tx.Account.Create().SetUserID(1).SetBalance(1000).Save(ctx)
if err != nil {
    tx.Rollback()
    log.Fatal(err)
}

err = tx.Commit()
if err != nil {
    tx.Rollback()
    log.Fatal(err)
}
```

##### 9.3.3 Transaction Management in XORM
In XORM, use the `NewSession` method:
```go
session := engine.NewSession()
defer session.Close()

err := session.Begin()
if err != nil {
    log.Fatal(err)
}

_, err = session.Insert(&User{Name: "Alice", Email: "alice@example.com"})
if err != nil {
    session.Rollback()
    log.Fatal(err)
}

_, err = session.Insert(&Account{UserID: 1, Balance: 1000})
if err != nil {
    session.Rollback()
    log.Fatal(err)
}

err = session.Commit()
if err != nil {
    session.Rollback()
    log.Fatal(err)
}
```

#### 9.4 Concurrency and Transaction Isolation Levels

In a database, the different transaction isolation levels define the visibility and concurrency control between transactions. Common isolation levels include:

- **Read Uncommitted**: A transaction can read data that other transactions have not yet committed, which may cause dirty reads.
- **Read Committed**: A transaction can only read data that other transactions have committed, which prevents dirty reads.
- **Repeatable Read**: Once a transaction starts, it can read data, and the data it sees stays consistent for the whole transaction; this prevents non-repeatable reads.
- **Serializable**: The highest level of isolation. Transactions run fully serially, which prevents phantom reads.

In Go's `database/sql` package, you can control concurrency behavior by setting the transaction's isolation level:
```go
txOptions := &sql.TxOptions{
    Isolation: sql.LevelSerializable,
}
tx, err := db.BeginTx(context.Background(), txOptions)
if err != nil {
    log.Fatal(err)
}
```

In ORM frameworks, you can likewise set transaction options to specify the isolation level.

#### 9.5 MVCC in MySQL

Multi-Version Concurrency Control (MVCC) is a technique for improving database concurrency performance. MySQL's InnoDB storage engine uses MVCC to implement the Repeatable Read isolation level, avoiding non-repeatable reads and, for the most part, avoiding phantom reads.

##### 9.5.1 MVCC Basics
- **Version chain**: Every row has multiple versions. InnoDB maintains the version chain through hidden columns `DB_TRX_ID` (the ID of the transaction that last modified the row) and `DB_ROLL_PTR` (the rollback pointer, pointing to the older version in the undo log).
- **Snapshot read**: Reads use a snapshot, so uncommitted data is never read.
- **Current read**: Modifications read the latest version, keeping data consistent.

##### 9.5.2 How MVCC Works
On a read, the InnoDB engine reads data according to the current transaction's snapshot version, avoiding conflicts with other transactions' writes. On a write, InnoDB creates a new data version and links it to the older version in the undo log through `DB_ROLL_PTR`, while writing a new `DB_TRX_ID`.

##### 9.5.3 MVCC Example
Suppose there is a `users` table holding user information. Read user data in transaction A:
```sql
START TRANSACTION;
SELECT * FROM users WHERE id = 1;
```

Modify the user data in transaction B:
```sql
START TRANSACTION;
UPDATE users SET name = 'Bob' WHERE id = 1;
```

Read the user data again in transaction A. Because it uses a snapshot read, transaction A still sees the version before the change:
```sql
SELECT * FROM users WHERE id = 1;
```

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)
- [Official · Database Transactions](https://go.dev/doc/database/execute-transactions)


## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [Sharding](/db/Sharding.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Sharding](/db/Sharding.md)
