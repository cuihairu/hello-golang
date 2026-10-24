###  Database sharding, distributed transactions, and consistency

#### 17.1 Database sharding

Database sharding splits the data of a large table horizontally across multiple database instances, so that each instance carries only part of the data and traffic, and the system's overall throughput scales up with the number of instances.

##### 17.1.1 The concept of sharding

Sharding spreads the data in a database across multiple physical databases according to some rule, achieving horizontal scaling. Common sharding strategies include horizontal sharding and vertical sharding.

##### 17.1.2 Sharding strategies

- **Horizontal sharding**: shard the data by the value of a certain field (such as a user ID). Each shard contains a table of the same structure but stores a different range of data.

  Example:
  ```plaintext
  Shard 1: user IDs 1-1000
  Shard 2: user IDs 1001-2000
  ```

- **Vertical sharding**: shard by the table's columns, storing the data of different columns in different databases. This approach suits tables with many columns that are accessed at different frequencies.

  Example:
  ```plaintext
  Shard 1: the users table's basic information columns (ID, name, email)
  Shard 2: the users table's extended information columns (address, phone)
  ```

- **Hybrid sharding**: combines horizontal and vertical sharding, distributing the data more finely across multiple databases.

##### 17.1.3 Implementing sharding

At the application layer, you can use a shard key (such as a user ID) to decide which shard the data goes to. For example, when inserting user data, compute the target shard from the user ID:

```go
type User struct {
    ID int
}

func getShard(userID int) int {
    if userID <= 1000 {
        return 1
    } else {
        return 2
    }
}

func insertUser(user User) {
    shard := getShard(user.ID)
    if shard == 1 {
        // insert into the users_1 table
    } else {
        // insert into the users_2 table
    }
}
```

##### 17.1.4 A sharding example

Suppose there is a users table that needs horizontal sharding. You can shard it by ranges of user ID:

```sql
-- Shard 1
CREATE TABLE users_1 (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
-- Shard 2
CREATE TABLE users_2 (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
```

Then insert the data with user IDs 1 to 1000 into the users_1 table, and the data with user IDs 1001 to 2000 into the users_2 table.

#### 17.2 Distributed transactions

Once the data is split across multiple nodes, a single-node transaction no longer covers it: operations spanning several nodes must either all succeed or all fail, which is exactly what distributed transactions exist to solve.

##### 17.2.1 Consistency models

- **Strong consistency**: the data on all nodes is always consistent, and every read returns the most recent data.
- **Eventual consistency**: the data reaches a consistent state after some time; suitable for scenarios that do not demand strong consistency but do need high availability.
- **Causal consistency**: guarantees the consistency of data that has a causal relationship, keeping the order of dependent operations intact.

##### 17.2.2 Distributed transactions

A distributed transaction is one that executes across multiple nodes of a distributed system, ensuring these operations either all succeed or all fail.

###### Two-phase commit (2PC)

Two-phase commit is a common distributed transaction protocol, split into a prepare phase and a commit phase:

1. **Prepare phase**:
   - The coordinator sends a prepare request to all participants.
   - Each participant performs the transaction operations without committing, records the operations in a log, and replies ready or failed.

2. **Commit phase**:
   - If all participants are ready, the coordinator sends a commit request to all participants, and they commit the transaction.
   - If any participant fails, the coordinator sends a rollback request to all participants, and they roll back the transaction.

Example code: a simple two-phase commit in Go
```go
type TransactionCoordinator struct {
    participants []Participant
}

type Participant interface {
    Prepare() error
    Commit() error
    Rollback() error
}

func (tc *TransactionCoordinator) Execute() error {
    for _, participant := range tc.participants {
        if err := participant.Prepare(); err != nil {
            tc.rollback()
            return err
        }
    }
    for _, participant := range tc.participants {
        if err := participant.Commit(); err != nil {
            tc.rollback()
            return err
        }
    }
    return nil
}

func (tc *TransactionCoordinator) rollback() {
    for _, participant := range tc.participants {
        participant.Rollback()
    }
}
```

###### Three-phase commit (3PC)

Three-phase commit adds a timeout mechanism to reduce blocking and improve the system's reliability:

1. **CanCommit phase**: the coordinator asks each participant whether it can commit, and the participant replies yes or no.
2. **PreCommit phase**: the coordinator tells the participants to prepare to commit, and they perform the transaction operations without committing.
3. **Commit phase**: the coordinator tells the participants to commit, and they commit the transaction.

#### 17.3 Database consistency

##### 17.3.1 Consistency models

In a distributed system, a consistency model describes how and when data is synchronized between nodes. Common consistency models include:

- **Strong consistency**: every read returns the most recent write.
- **Eventual consistency**: all replicas in the system eventually reach the same state, though there may be a brief period of inconsistency.
- **Causal consistency**: the order of causally related operations stays consistent.

##### 17.3.2 The CAP theorem

The CAP theorem states that a distributed system cannot satisfy all three of the following at once: consistency (Consistency), availability (Availability), and partition tolerance (Partition Tolerance). You can only trade off between any two of them.

- **Consistency**: all nodes have the same data at the same time.
- **Availability**: every request receives a non-error response, without guaranteeing the latest data.
- **Partition tolerance**: the system keeps working even when a network partition occurs.

##### 17.3.3 The BASE theory

The BASE theory is a theory of basic availability and eventual consistency, used to handle consistency problems in distributed systems. It comprises:

- **Basically Available**: when a fault occurs, the system allows part of its functionality to degrade.
- **Soft State**: the system's state can differ between nodes, and does not require strong consistency.
- **Eventually Consistent**: the data in the system eventually reaches a consistent state after some time.

#### 17.4 Implementing distributed transactions

##### 17.4.1 The XA protocol

The XA protocol is a distributed transaction protocol that defines the interfaces for distributed transaction management. It has two parts: the transaction manager (Transaction Manager) and the resource manager (Resource Manager). The transaction manager coordinates distributed transactions, and the resource manager manages the specific resources (such as a database).

##### 17.4.2 The TCC model

The TCC (Try-Confirm-Cancel) model is a distributed transaction solution with three stages:

1. **Try stage**: attempt the business operation and reserve the resources.
2. **Confirm stage**: confirm the operation and commit the transaction.
3. **Cancel stage**: cancel the operation and release the resources.

Example code: the TCC model in Go
```go
type TCCParticipant interface {
    Try() error
    Confirm() error
    Cancel() error
}

type TCCCoordinator struct {
    participants []TCCParticipant
}

func (tc *TCCCoordinator) Execute() error {
    for _, participant := range tc.participants {
        if err := participant.Try(); err != nil {
            tc.cancel()
            return err
        }
    }
    for _, participant := range tc.participants {
        if err := participant.Confirm(); err != nil {
            tc.cancel()
            return err
        }
    }
    return nil
}

func (tc *TCCCoordinator) cancel() {
    for _, participant := range tc.participants {
        participant.Cancel()
    }
}
```

##### 17.4.3 The Saga pattern

The Saga pattern is a pattern for managing long-running transactions: it breaks a long transaction into a series of short transactions, each with its own compensation operation. There are two kinds of Saga:

1. **Sequential execution**: run each short transaction in order, and when one fails, run the corresponding compensation.
2. **Parallel execution**: run multiple short transactions in parallel, and when one fails, run the corresponding compensation.

Example code: the Saga pattern in Go
```go
type SagaStep struct {


    Action    func() error
    Compensate func() error
}

type Saga struct {
    steps []SagaStep
}

func (s *Saga) Execute() error {
    var executedSteps []SagaStep
    for _, step := range s.steps {
        if err := step.Action(); err != nil {
            s.compensate(executedSteps)
            return err
        }
        executedSteps = append(executedSteps, step)
    }
    return nil
}

func (s *Saga) compensate(executedSteps []SagaStep) {
    for i := len(executedSteps) - 1; i >= 0; i-- {
        executedSteps[i].Compensate()
    }
}
```

To wrap up in one line: sharding decides where the data goes, CAP sets the ceiling on what you can design, and 2PC/3PC, TCC, and Saga are a few paths ordered by consistency strength and implementation cost - which one you take depends on how long an intermediate state your business can tolerate.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)


## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [Security](/db/Security.md)
- [Tx](/db/Tx.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Security](/db/Security.md)
- [Tx](/db/Tx.md)
