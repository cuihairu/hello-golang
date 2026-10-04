# 滑动窗口

滑动窗口（Sliding Window）是网络传输和流量控制中的核心概念，同时也是一种常用的限流算法。本节分别介绍 TCP 中的滑动窗口机制，以及如何在 Go 中实现基于滑动窗口的限流器。

### TCP 中的滑动窗口

TCP 使用滑动窗口实现流量控制与可靠传输：

- **发送窗口**：发送方维护一个窗口，窗口内的字节可以连续发送而无需逐个等待确认（ACK）。窗口左边界由接收方确认的字节推进，右边界由对端通告的接收窗口（rwnd）决定。
- **接收窗口**：接收方通过 TCP 头部中的 window 字段告知发送方自己还能接收多少数据，从而防止发送方淹没接收方的缓冲区。
- **滑动过程**：收到 ACK 后窗口向前"滑动"，新的数据进入窗口可被发送。窗口大小 = min(rwnd, cwnd)（接收窗口与拥塞窗口的较小值）。

```
已确认     [ 可发送但未确认 | 未发送 ]        不可发送
已发送 <---+----------------------------+---> 序号空间
                <------ 发送窗口 ------>
                 窗口随 ACK 不断右移
```

### 应用层：滑动窗口限流器

作为限流算法，滑动窗口相比固定窗口计数器没有"窗口边界突刺"问题：统计最近 N 秒内的请求数，超过阈值则拒绝。

下面的实现用循环队列（环形缓冲区）存窗口内每个请求的时间戳：每次判断先淘汰过期记录，再看有没有空位，队列长度固定为 `limit`：

```go
package main

import (
	"fmt"
	"sync"
	"time"
)

// SlidingWindowLimiter 基于滑动窗口的限流器：
// 在 window 时间内最多允许 limit 次请求
type SlidingWindowLimiter struct {
	mu      sync.Mutex
	limit   int           // 窗口内允许的最大请求数
	window  time.Duration // 窗口长度
	stamps  []time.Time   // 循环队列，保存窗口内请求的时间戳
	head    int           // 队列头下标
	count   int           // 队列中的有效元素个数
}

func NewSlidingWindowLimiter(limit int, window time.Duration) *SlidingWindowLimiter {
	return &SlidingWindowLimiter{
		limit:  limit,
		window: window,
		stamps: make([]time.Time, limit),
	}
}

// Allow 判断当前请求是否被允许
func (l *SlidingWindowLimiter) Allow() bool {
	now := time.Now()
	l.mu.Lock()
	defer l.mu.Unlock()

	// 淘汰窗口之外的过期请求
	for l.count > 0 && now.Sub(l.stamps[l.head]) >= l.window {
		l.head = (l.head + 1) % len(l.stamps)
		l.count--
	}

	if l.count >= l.limit {
		return false // 窗口内请求数已满，拒绝
	}

	// 记录本次请求（队列未满，tail 位置必然为空）
	tail := (l.head + l.count) % len(l.stamps)
	l.stamps[tail] = now
	l.count++
	return true
}

func main() {
	// 1 秒内最多允许 5 次请求
	limiter := NewSlidingWindowLimiter(5, time.Second)

	for i := 1; i <= 8; i++ {
		if limiter.Allow() {
			fmt.Printf("请求 %d: 通过\n", i)
		} else {
			fmt.Printf("请求 %d: 被限流\n", i)
		}
		time.Sleep(100 * time.Millisecond)
	}

	// 等待窗口滑过，请求恢复
	time.Sleep(800 * time.Millisecond)
	fmt.Println("等待窗口滑过后:")
	if limiter.Allow() {
		fmt.Println("请求 9: 通过")
	}
}
```

输出示例：

```
请求 1: 通过
请求 2: 通过
请求 3: 通过
请求 4: 通过
请求 5: 通过
请求 6: 被限流
请求 7: 被限流
请求 8: 被限流
等待窗口滑过后:
请求 9: 通过
```

### 与其他限流算法的对比

| 算法 | 特点 | 缺点 |
| ---- | ---- | ---- |
| 固定窗口计数器 | 实现最简单 | 窗口边界处可能出现两倍突发流量 |
| 滑动窗口日志（本节实现） | 精确，无边界突刺 | 需要记录每个请求，高并发下内存开销较大 |
| 滑动窗口计数 | 把窗口切成小格子近似滑动，内存开销小 | 精度取决于格子数量 |
| 令牌桶 | 允许一定突发，平滑控制平均速率 | 需要后台生成令牌或惰性计算 |

### 总结

TCP 的滑动窗口解决了"发送多快合适"的问题，而应用层的滑动窗口限流解决的是"单位时间允许多少请求"的问题。两者的共同思想是：用一个随时间滑动的区间来度量近期的行为，而不是孤立地看待每个时刻。在 Go 服务中，滑动窗口限流器常用于 API 网关、中间件和客户端重试控制等场景。
