### 竞争条件（Race Condition）

竞争条件是指当多个线程或进程并发地访问和修改共享资源，并且最终的结果依赖于这些访问操作的执行顺序时，就会发生竞争条件。竞争条件可能导致程序出现不一致的数据或未定义的行为。简单来说，当两个或多个线程同时访问共享资源时，如果不进行适当的同步，就可能导致数据冲突。

### Go中的竞争条件示例

Go 鼓励并发编程，竞争条件也就更常见。先看一个会出问题的例子，再给它加上同步。

#### 竞争条件的例子

```go
package main

import (
	"fmt"
	"sync"
)

var counter int

func increment(wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 0; i < 1000; i++ {
		counter++
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

在这个例子中，多个Goroutine并发地执行`increment`函数，每个函数都会增加`counter`的值。由于没有同步机制，多个Goroutine可能会同时访问和修改`counter`，导致竞争条件。运行这段代码多次，最终的`counter`值可能每次都不同，因为它依赖于Goroutine的执行顺序。

#### 使用互斥锁解决竞争条件

为了避免竞争条件，可以使用互斥锁（Mutex）来确保在同一时间只有一个Goroutine可以访问和修改共享资源。下面是修改后的例子，使用互斥锁来同步对`counter`的访问。

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
		mu.Lock()
		counter++
		mu.Unlock()
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

在这个修改后的例子中，使用了`sync.Mutex`来创建一个互斥锁`mu`。在每次修改`counter`之前，先使用`mu.Lock()`获取锁，修改完成后使用`mu.Unlock()`释放锁。这样可以确保在同一时间只有一个Goroutine可以修改`counter`，从而避免了竞争条件。

运行这段代码，无论多少次，最终的`counter`值应该总是10000（因为10个Goroutine，每个增加1000次）。

### 竞态检测工具

Go提供了一个内置的竞态检测工具，可以在运行时检测程序中的竞态条件。在运行程序时，可以使用`-race`标志来启用竞态检测：

```sh
go run -race main.go
```

启用后，只要运行路径上真的发生了并发冲突访问，`-race` 就会把两个冲突的读写位置打印出来。并发代码合入前建议都过一遍 `-race`。