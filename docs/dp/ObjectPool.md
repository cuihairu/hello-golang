### 对象池模式 (Object Pool Pattern)

#### 意图
对象池模式是一种创建型设计模式，它预先创建并维护一组已初始化的对象，需要时从池中取出，用完归还池中复用，而不是随用随建、用完即弃。对于创建成本高（如数据库连接、网络连接、大型缓冲区）或创建频率极高的轻量对象，复用可以显著减少分配、初始化和垃圾回收的开销。

#### 问题
在现实世界中，考虑一个访问数据库的应用。建立一次数据库连接需要 TCP 握手、认证等多个步骤，开销较大；如果每个请求都新建连接，高并发下系统资源会迅速耗尽。反过来，连接数量不加以限制，也可能把数据库压垮。

#### 解决方案
使用对象池模式，我们引入一个管理对象生命周期的池：

1. 池在初始化时（或首次取用时）通过工厂函数创建对象。
2. 借用者通过 `Acquire` 从池中取出空闲对象；池为空时创建新对象（或等待、或返回失败）。
3. 使用完毕后通过 `Release` 归还对象，池可以先重置对象状态再放回空闲队列，供下次复用。
4. 池对对象总数设上限，避免无限制地占用资源。

#### 模式结构
1. **资源对象（Reusable）**：被池管理的对象，例如连接、缓冲区。
2. **对象池（Object Pool）**：维护空闲对象集合，提供 `Acquire`（借出）和 `Release`（归还）方法，内部通过工厂函数创建新对象，并可在归还时重置状态。
3. **客户端（Client）**：从池中借出对象，使用完毕后归还，不直接创建或销毁对象。

#### 代码
以下是使用Go语言实现的对象池模式示例：

```go
package main

import (
	"fmt"
	"sync"
)

// DBConn 是被池管理的资源对象
type DBConn struct {
	ID int
}

func (c *DBConn) Query(sql string) {
	fmt.Printf("连接 %d 执行查询: %s\n", c.ID, sql)
}

// Pool 是通用对象池
type Pool struct {
	mu      sync.Mutex
	idle    []*DBConn
	nextID  int
	maxSize int
}

func NewPool(maxSize int) *Pool {
	return &Pool{maxSize: maxSize}
}

// Acquire 借出一个对象：池中有空闲对象就复用，否则在未达上限时创建新对象
func (p *Pool) Acquire() (*DBConn, error) {
	p.mu.Lock()
	defer p.mu.Unlock()

	if n := len(p.idle); n > 0 {
		conn := p.idle[n-1]
		p.idle = p.idle[:n-1]
		return conn, nil
	}
	if p.nextID >= p.maxSize {
		return nil, fmt.Errorf("对象池已满，最多 %d 个对象", p.maxSize)
	}
	p.nextID++
	return &DBConn{ID: p.nextID}, nil
}

// Release 归还对象，放回空闲队列供下次复用
func (p *Pool) Release(conn *DBConn) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.idle = append(p.idle, conn)
}

func main() {
	pool := NewPool(2)

	// 借出两个连接
	conn1, _ := pool.Acquire()
	conn2, _ := pool.Acquire()

	conn1.Query("SELECT * FROM users")
	conn2.Query("SELECT * FROM orders")

	// 归还后再次借出，得到的是同一个对象（复用）
	pool.Release(conn1)
	conn3, _ := pool.Acquire()
	fmt.Println("复用连接:", conn3 == conn1)

	// 已达上限，再借出会失败
	if _, err := pool.Acquire(); err != nil {
		fmt.Println("借出失败:", err)
	}
}
```

输出：

```
连接 1 执行查询: SELECT * FROM users
连接 2 执行查询: SELECT * FROM orders
复用连接: true
借出失败: 对象池已满，最多 2 个对象
```

### 使用标准库 sync.Pool

Go 标准库提供了 `sync.Pool`，用于复用临时对象，减轻垃圾回收压力。它常用于高频分配的场景（如序列化缓冲区）：

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

			// 借出缓冲区
			buf := bufPool.Get().(*bytes.Buffer)
			defer func() {
				buf.Reset() // 归还前重置状态
				bufPool.Put(buf)
			}()

			fmt.Fprintf(buf, "goroutine %d 的输出", id)
			fmt.Println(buf.String())
		}(i)
	}

	wg.Wait()
}
```

注意：`sync.Pool` 中的对象可能在任意时刻被垃圾回收器清除，不能用于存放连接这类必须长期持有的资源；它只适合复用"丢了也无妨"的临时对象。需要持久化、可计数的资源池（如数据库连接池）应使用 `database/sql` 内置的连接池，协程池场景可选 `github.com/panjf2000/ants`、`github.com/alitto/pond` 等第三方实现。

#### 适用场景
- 对象创建成本高，如数据库连接、网络连接、线程。
- 高频创建、销毁大量短生命周期对象，垃圾回收压力大。
- 需要限制资源总数，防止并发过载。

#### 实现方式
1. 定义资源对象类型，并确保它可以被重置到可用状态。
2. 实现对象池，维护空闲对象集合，提供借出和归还方法；借出时可用工厂函数或 `sync.Pool` 的 `New` 创建新对象。
3. 归还前重置对象状态，避免上一个使用者的数据残留到下次借用。
4. 客户端从池中借出对象，使用后务必归还（通常配合 `defer`）。

#### 优缺点
**优点**：
- 复用对象，减少创建、销毁和垃圾回收的开销，提高性能。
- 可以限制对象总数，避免资源被耗尽。

**缺点**：
- 归还的对象必须正确重置，否则会把脏状态带给下一个使用者。
- 对象数量和池的管理逻辑增加了系统复杂性；对象闲置时占用内存。
- 借出后忘记归还会导致资源泄漏（池对象被占满）。

#### 其他模式的关系
- **单例模式（Singleton Pattern）**：对象池本身通常以单例形式存在，全局只维护一个池。
- **享元模式（Flyweight Pattern）**：两者都通过共享对象节省资源，但享元模式共享的是不可变的"状态"，而对象池中的对象借出后会被独占使用。
- **工厂模式（Factory Pattern）**：对象池在需要新对象时依赖工厂（函数）来创建对象。
