# Read-write mutex

A read-write mutex separates "read" and "write" access: multiple goroutines can hold the read lock at the same time and read concurrently, but the write lock is exclusive — while it is held, every other read and write is blocked; and while a write lock is waiting, no new read locks can join, so a writer is not starved indefinitely by a steady stream of arriving readers. This makes the read-write mutex especially well suited to read-heavy, write-rare scenarios (configuration, caches, routing tables), where it can give higher concurrency than an ordinary mutex.

### The methods of sync.RWMutex

The Go standard library `sync.RWMutex` provides the following methods:

| Method | Description |
| --- | --- |
| `RLock()` | Acquire the read lock, compatible with other read locks; blocks if a write lock is held (or waiting) |
| `RUnlock()` | Release the read lock |
| `Lock()` | Acquire the write lock, exclusive; waits for all read and write locks to be released |
| `Unlock()` | Release the write lock |
| `TryRLock()` | Try to acquire the read lock (Go 1.18+), returns `false` immediately on failure |
| `TryLock()` | Try to acquire the write lock (Go 1.18+), returns `false` immediately on failure |
| `RLocker()` | Returns a `sync.Locker` that maps `RLock`/`RUnlock` to `Lock`/`Unlock`, so it can be combined with APIs that need a `sync.Locker` (such as `sync.Cond`) |

### A typical example: a concurrency-safe cache

Reads go through the read lock, so many requests can read at the same time; writes go through the write lock, guaranteeing no concurrent access while the data is being modified:

```go
package main

import (
	"fmt"
	"sync"
)

type Cache struct {
	mu   sync.RWMutex
	data map[string]string
}

func NewCache() *Cache {
	return &Cache{data: make(map[string]string)}
}

// Get only needs the read lock, so multiple goroutines can read at the same time
func (c *Cache) Get(key string) string {
	c.mu.RLock()
	defer c.mu.RUnlock()
	return c.data[key]
}

// Set needs the write lock; while it writes, every other read and write is blocked
func (c *Cache) Set(key, value string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.data[key] = value
}

func main() {
	cache := NewCache()
	cache.Set("go", "golang")

	var wg sync.WaitGroup

	// 5 concurrent reads
	for i := 1; i <= 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			fmt.Printf("reader %d: %s\n", id, cache.Get("go"))
		}(i)
	}

	// 1 concurrent write
	wg.Add(1)
	go func() {
		defer wg.Done()
		cache.Set("rust", "rustlang")
	}()

	wg.Wait()
	fmt.Println(cache.Get("go"), cache.Get("rust"))
}
```

### Things to watch out for

1. **No upgrade**: if the same goroutine calls `Lock()` while already holding the read lock, it blocks forever — the write lock has to wait for all read locks to be released, and the read lock it is waiting for is its own. This kind of "lock upgrade" must `RUnlock()` first and then `Lock()`, or you should switch to a plain `sync.Mutex`.

2. **The lock cannot be copied**: like `sync.Mutex`, an `RWMutex` must not be copied by value once it has been used; a struct containing it should be passed by pointer.

3. **Do not protect read-only data with a lock**: data that no longer changes after initialization has no concurrent writes, so just read it directly; adding a read-write lock only brings overhead for nothing.

4. **It only pays off when writes are rare**: `RWMutex` has more internal state than `Mutex`, and switching between reads and writes costs something in itself. If the read/write ratio is close to even, `sync.Mutex` is often faster and simpler.

### Summary

`sync.RWMutex` raises concurrency in read-heavy, write-rare scenarios through "shared reads, exclusive writes": use `RLock`/`RUnlock` for reads, `Lock`/`Unlock` for writes, and `TryLock`/`TryRLock` for non-blocking attempts when needed. Keep in mind that the lock cannot be upgraded and cannot be copied, and only pick it when the read/write ratio suits it, so you actually get its advantage.

## References

- [sync standard library](https://pkg.go.dev/sync)
- [Go memory model](https://go.dev/ref/mem)
- [Official blog · Introducing the Go Race Detector](https://go.dev/blog/race-detector)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
- [Primitives](/sync/Primitives.md)
