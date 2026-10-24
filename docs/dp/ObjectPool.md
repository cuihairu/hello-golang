### Object Pool Pattern

#### Intent
The Object Pool Pattern is a creational design pattern: pre-create and maintain a set of already-initialized objects, take them from the pool when needed, and return them when done to reuse — instead of building one on each use and discarding it after. For objects that are expensive to create (database connections, network connections, large buffers) or lightweight objects that are created very frequently, reuse saves the repeated cost of allocating, initializing, and garbage-collecting.

#### Problem
In the real world, consider an application that accesses a database. Establishing a database connection takes several steps — a TCP handshake, authentication, and so on — and is costly. If every request opens a new connection, system resources get exhausted quickly under high concurrency. Conversely, if connection count is left unlimited, the database itself can be overwhelmed.

#### Solution
The Object Pool Pattern introduces a pool that manages the objects' lifecycle:

1. On initialization (or on first checkout), the pool creates objects via a factory function.
2. A borrower takes an idle object from the pool via `Acquire`; when the pool is empty, a new object is created (or it waits, or it returns failure).
3. After use, the object is returned via `Release`; the pool can reset the object's state before putting it back in the idle queue for reuse.
4. The pool caps the total number of objects to avoid unbounded resource consumption.

#### Structure
1. **Reusable**: the object managed by the pool, such as a connection or buffer.
2. **Object Pool**: maintains the set of idle objects, provides `Acquire` (check out) and `Release` (return) methods, creates new objects internally via a factory function, and can reset state on return.
3. **Client**: checks out objects from the pool and returns them after use, without creating or destroying objects directly.

#### Code
Go implementation:

```go
package main

import (
	"fmt"
	"sync"
)

// DBConn is the resource object managed by the pool
type DBConn struct {
	ID int
}

func (c *DBConn) Query(sql string) {
	fmt.Printf("connection %d runs query: %s\n", c.ID, sql)
}

// Pool is a generic object pool
type Pool struct {
	mu      sync.Mutex
	idle    []*DBConn
	nextID  int
	maxSize int
}

func NewPool(maxSize int) *Pool {
	return &Pool{maxSize: maxSize}
}

// Acquire checks out an object: reuse an idle one if available, otherwise create a new one while under the limit
func (p *Pool) Acquire() (*DBConn, error) {
	p.mu.Lock()
	defer p.mu.Unlock()

	if n := len(p.idle); n > 0 {
		conn := p.idle[n-1]
		p.idle = p.idle[:n-1]
		return conn, nil
	}
	if p.nextID >= p.maxSize {
		return nil, fmt.Errorf("pool full, max %d objects", p.maxSize)
	}
	p.nextID++
	return &DBConn{ID: p.nextID}, nil
}

// Release returns the object, putting it back in the idle queue for reuse
func (p *Pool) Release(conn *DBConn) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.idle = append(p.idle, conn)
}

func main() {
	pool := NewPool(2)

	// check out two connections
	conn1, _ := pool.Acquire()
	conn2, _ := pool.Acquire()

	conn1.Query("SELECT * FROM users")
	conn2.Query("SELECT * FROM orders")

	// after returning, checking out again yields the same object (reuse)
	pool.Release(conn1)
	conn3, _ := pool.Acquire()
	fmt.Println("reused connection:", conn3 == conn1)

	// at the limit, checking out again fails
	if _, err := pool.Acquire(); err != nil {
		fmt.Println("acquire failed:", err)
	}
}
```

Output:

```
connection 1 runs query: SELECT * FROM users
connection 2 runs query: SELECT * FROM orders
reused connection: true
acquire failed: pool full, max 2 objects
```

### Using the standard library sync.Pool

The Go standard library provides `sync.Pool` for reusing temporary objects and reducing garbage-collection pressure. It is commonly used in high-frequency allocation scenarios (such as serialization buffers):

```go
package main

import (
	"bytes"
	"fmt"
	"sync"
)

var bufPool = sync.Pool{
	New: func() interface{} {
		return new(bytes.Buffer)
	},
}

func main() {
	var wg sync.WaitGroup

	for i := 0; i < 3; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()

			// check out a buffer
			buf := bufPool.Get().(*bytes.Buffer)
			defer func() {
				buf.Reset() // reset state before returning
				bufPool.Put(buf)
			}()

			fmt.Fprintf(buf, "output of goroutine %d", id)
			fmt.Println(buf.String())
		}(i)
	}

	wg.Wait()
}
```

Note: objects in `sync.Pool` may be cleared by the garbage collector at any time, so it cannot be used to hold resources that must be kept long-term, like connections; it is only suitable for reusing temporary objects where losing one is harmless. For persistent, countable resource pools (like a database connection pool), use the built-in connection pool in `database/sql`; for goroutine-pool scenarios, third-party implementations such as `github.com/panjf2000/ants` or `github.com/alitto/pond` are options.

#### Applicable scenarios
- Object creation is costly, such as database connections, network connections, or threads.
- High-frequency creation and destruction of many short-lived objects, putting pressure on garbage collection.
- You need to cap the total number of resources to prevent concurrency overload.

#### Implementation
1. Define the resource object type and make sure it can be reset to a usable state.
2. Implement the object pool, maintaining the set of idle objects and providing check-out and return methods; on checkout, use a factory function or `sync.Pool`'s `New` to create a new object.
3. Reset the object's state before returning it, so the previous user's data does not leak into the next checkout.
4. The client checks out objects from the pool and must always return them after use (typically paired with `defer`).

#### Pros and cons
**Pros**:
- Reuses objects, reducing creation, destruction, and garbage-collection overhead, improving performance.
- Caps the total number of objects, avoiding resource exhaustion.

**Cons**:
- Returned objects must be reset correctly, otherwise dirty state gets passed to the next user.
- The object count and pool management logic add system complexity; idle objects still occupy memory.
- Forgetting to return after checkout causes a resource leak (the pool gets filled up).

#### Relationship to other patterns
- **Singleton Pattern**: the object pool itself typically exists as a singleton, with only one pool maintained globally.
- **Flyweight Pattern**: both save resources by sharing objects, but the flyweight pattern shares immutable "state," while objects in a pool are used exclusively once checked out.
- **Factory Pattern**: when the pool needs a new object, it relies on a factory (function) to create it.

## References

- [GoF "Design Patterns" Overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru Design Patterns Catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Memento](/dp/Memento.md)
- [Observer](/dp/Observer.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Memento](/dp/Memento.md)
- [Observer](/dp/Observer.md)
