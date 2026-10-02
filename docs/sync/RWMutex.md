# 读写锁

读写锁把"读"和"写"两种访问区分开：多个 Goroutine 可以同时持有读锁并发读取，但写锁是独占的——写锁被持有期间，其他读和写都会被阻塞；写锁等待期间，新的读锁也无法加入，避免写者被持续到来的读者无限期饿死。这种特性使读写锁特别适合读多写少的场景（如配置、缓存、路由表），可以比普通互斥锁获得更高的并发度。

### sync.RWMutex 的方法

Go 标准库 `sync.RWMutex` 提供以下方法：

| 方法 | 说明 |
| --- | --- |
| `RLock()` | 获取读锁，与其他读锁兼容；已有写锁（或写锁在等待）时阻塞 |
| `RUnlock()` | 释放读锁 |
| `Lock()` | 获取写锁，独占；等所有读锁和写锁释放 |
| `Unlock()` | 释放写锁 |
| `TryRLock()` | 尝试获取读锁（Go 1.18+），失败立即返回 `false` |
| `TryLock()` | 尝试获取写锁（Go 1.18+），失败立即返回 `false` |
| `RLocker()` | 返回一个把 `RLock`/`RUnlock` 映射为 `Lock`/`Unlock` 的 `sync.Locker`，便于与需要 `sync.Locker` 的 API（如 `sync.Cond`）配合使用 |

### 典型示例：并发安全的缓存

读操作走读锁，多个请求可以同时读；写操作走写锁，保证修改期间没有并发访问：

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

// Get 只需要读锁，多个 goroutine 可以同时读取
func (c *Cache) Get(key string) string {
	c.mu.RLock()
	defer c.mu.RUnlock()
	return c.data[key]
}

// Set 需要写锁，写入期间其他读和写都会被阻塞
func (c *Cache) Set(key, value string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.data[key] = value
}

func main() {
	cache := NewCache()
	cache.Set("go", "golang")

	var wg sync.WaitGroup

	// 5 个并发读
	for i := 1; i <= 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			fmt.Printf("reader %d: %s\n", id, cache.Get("go"))
		}(i)
	}

	// 1 个并发写
	wg.Add(1)
	go func() {
		defer wg.Done()
		cache.Set("rust", "rustlang")
	}()

	wg.Wait()
	fmt.Println(cache.Get("go"), cache.Get("rust"))
}
```

### 使用注意事项

1. **不可升级**：同一个 Goroutine 在持有读锁的情况下再调用 `Lock()` 会永久阻塞——写锁必须等所有读锁释放，而它要等的正是自己。这种"锁升级"必须先 `RUnlock()` 再 `Lock()`，或者改用一个普通 `sync.Mutex`。

2. **锁不可拷贝**：与 `sync.Mutex` 一样，`RWMutex` 使用后不能按值复制，包含它的结构体应通过指针传递。

3. **不要用锁保护只读数据**：初始化完成后不再变化的数据没有并发写，直接读取即可，加读写锁反而白白引入开销。

4. **写少读多才划算**：`RWMutex` 内部状态比 `Mutex` 复杂，读写切换本身有成本。如果读写比例接近，`sync.Mutex` 往往更快、更简单。

### 小结

`sync.RWMutex` 通过"读共享、写独占"提升了读多写少场景下的并发性能：读用 `RLock`/`RUnlock`，写用 `Lock`/`Unlock`，必要时用 `TryLock`/`TryRLock` 做非阻塞尝试。使用时注意锁不可升级、不可拷贝，并在读写比例合适时选择它，才能发挥其优势。
