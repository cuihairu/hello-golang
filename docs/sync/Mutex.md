### 互斥锁（Mutex）

互斥锁是同步机制：同一时刻只放一个线程进入临界区，用来挡住竞争条件（Race Conditions）。

### Go中的互斥锁

在Go语言中，互斥锁由标准库`sync`包提供。常用的类型是`sync.Mutex`，它有两个主要方法：

- `Lock()`: 加锁，如果锁已经被持有，调用此方法的Goroutine会阻塞，直到锁被释放。
- `Unlock()`: 解锁，释放锁，使其他阻塞的Goroutine可以获得锁。释放一把未被持有的锁会直接 panic（`sync: unlock of unlocked mutex`）。
- `TryLock()`（Go 1.18+）: 尝试加锁，成功返回 `true`；锁被占用则立即返回 `false`，不会等待。

#### 互斥锁的例子

下面这个例子用 `sync.Mutex` 保护一个 `counter`：

```go
package main

import (
	"fmt"
	"sync"
)

var (
	counter int
	mu      sync.Mutex
)

func increment(wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 0; i < 1000; i++ {
		mu.Lock()   // 加锁，进入临界区
		counter++
		mu.Unlock() // 解锁，离开临界区
	}
}

func main() {
	var wg sync.WaitGroup

	for i := 0; i < 10; i++ {
		wg.Add(1)
		go increment(&wg)
	}

	wg.Wait()
	fmt.Println("Final Counter:", counter)
}
```

#### 代码解释

1. **定义互斥锁和共享变量**：
    ```go
    var (
        counter int
        mu      sync.Mutex
    )
    ```

2. **使用互斥锁保护临界区**：
    ```go
    func increment(wg *sync.WaitGroup) {
        defer wg.Done()
        for i := 0; i < 1000; i++ {
            mu.Lock()   // 加锁，进入临界区
            counter++
            mu.Unlock() // 解锁，离开临界区
        }
    }
    ```

3. **主函数**：
    ```go
    func main() {
        var wg sync.WaitGroup

        for i := 0; i < 10; i++ {
            wg.Add(1)
            go increment(&wg)
        }

        wg.Wait()
        fmt.Println("Final Counter:", counter)
    }
    ```

在主函数中，启动了10个Goroutine，每个Goroutine执行`increment`函数，这些函数并发地增加`counter`的值。由于`counter`的访问被互斥锁保护，所以在所有Goroutine执行完毕后，`counter`的最终值总是正确的，即`10 * 1000 = 10000`。

### 用 TryLock 非阻塞获取

某些场景下，拿不到锁时更适合先去做别的事情，而不是干等。这时可以用 `TryLock`：

```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	var mu sync.Mutex

	mu.Lock() // 先持有锁，模拟锁被占用

	if mu.TryLock() {
		fmt.Println("获取到锁")
		mu.Unlock()
	} else {
		fmt.Println("锁被占用，先去做别的事")
	}

	mu.Unlock()
}
```

输出：

```
锁被占用，先去做别的事
```

### 使用规范

1. **加锁与解锁必须成对出现**：重复 `Unlock` 或解锁未加锁的锁都会 panic。分支多的函数建议写法固定为：

   ```go
   var mu sync.Mutex

   mu.Lock()
   defer mu.Unlock()
   ```

2. **不要重复加锁**：`sync.Mutex` 不可重入，同一个 Goroutine 两次 `Lock()` 会永久阻塞。

3. **不要拷贝锁**：互斥锁通过内部状态实现互斥，按值拷贝后各副本互不相干。锁应作为指针在函数间传递，包含锁的结构体也不要按值传递。下面的代码会被 `go vet` 检查出来：

   ```go
   type Counter struct {
       mu sync.Mutex
       n  int
   }

   // 错误：按值接收者会拷贝锁
   // func (c Counter) BadInc() { c.mu.Lock(); c.n++; c.mu.Unlock() }

   // 正确：使用指针接收者
   func (c *Counter) Inc() {
       c.mu.Lock()
       defer c.mu.Unlock()
       c.n++
   }
   ```

4. **保持锁的持有时间尽量短**：临界区只放必要的共享数据访问，I/O、耗时计算应移到锁外。

5. **多锁场景加锁顺序要一致**：需要同时持有多个锁时，所有 Goroutine 按相同顺序加锁，否则互相等待会形成死锁。

### 小结

`sync.Mutex` 的 `Lock`/`Unlock` 把临界区夹住，锁被占着时，别的 goroutine 会阻塞在 `Lock` 上。上例 10 个 goroutine 各加 1000 次，`counter` 最终是 10000；去掉 `Lock`/`Unlock`，结果就不一定是这个数了。拿不到锁不想干等用 `TryLock`；锁不可重入、不可拷贝这两条约定要记牢，能避开互斥锁的常见 bug。