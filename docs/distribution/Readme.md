# 分布式系统

分布式系统是由多台通过网络连接的机器协同对外提供服务的系统。Go 语言凭借轻量级的并发模型、静态编译的部署方式和出色的网络编程支持，成为构建分布式系统（etcd、Kubernetes、Consul、TiKV 等知名分布式系统均由 Go 编写）的主流语言。本章介绍分布式系统的核心问题域，以及 Go 在其中的典型应用方式。

### 分布式系统要解决的核心问题

1. **不可靠的网络**：节点之间的消息可能延迟、乱序或丢失，任何调用都必须考虑超时与重试。
2. **部分失败**：集群中某些节点宕机时，系统整体仍需可用，这与单机程序"要么全崩要么全好"的行为截然不同。
3. **时钟与顺序**：不同机器的时钟不一致，不能依赖全局时间来判断事件顺序，需要逻辑时钟或共识协议建立全序。
4. **数据一致性**：多副本之间的数据如何保持一致，是强一致（线性一致）、最终一致，还是介于两者之间。
5. **可扩展性**：通过数据分片（sharding）与负载均衡，让系统能够水平扩展。

### 常见的分布式模式与 Go 实现

#### 1. 心跳与故障检测

节点定期上报心跳，监控方在超时未收到心跳时判定节点故障。Go 的 `time.Ticker` 与 goroutine 天然适合这类周期任务：

```go
package main

import (
	"fmt"
	"sync"
	"time"
)

// NodeStatus 记录各节点的最后心跳时间
type NodeStatus struct {
	mu       sync.Mutex
	lastBeat map[string]time.Time
	timeout  time.Duration
}

func NewNodeStatus(timeout time.Duration) *NodeStatus {
	return &NodeStatus{lastBeat: make(map[string]time.Time), timeout: timeout}
}

func (s *NodeStatus) Beat(node string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.lastBeat[node] = time.Now()
}

func (s *NodeStatus) Alive(node string) bool {
	s.mu.Lock()
	defer s.mu.Unlock()
	last, ok := s.lastBeat[node]
	return ok && time.Since(last) <= s.timeout
}

func main() {
	status := NewNodeStatus(200 * time.Millisecond)
	status.Beat("node-1") // 启动时先上报一次心跳

	// 模拟节点 "node-1" 每 100ms 发一次心跳
	stop := make(chan struct{})
	go func() {
		ticker := time.NewTicker(100 * time.Millisecond)
		defer ticker.Stop()
		for {
			select {
			case <-ticker.C:
				status.Beat("node-1")
			case <-stop:
				return
			}
		}
	}()

	fmt.Println("node-1 存活:", status.Alive("node-1")) // true
	fmt.Println("node-2 存活:", status.Alive("node-2")) // false（从未心跳）

	time.Sleep(300 * time.Millisecond)
	close(stop)
	time.Sleep(300 * time.Millisecond)
	fmt.Println("node-1 心跳停止后存活:", status.Alive("node-1")) // false
}
```

#### 2. 分布式锁

多个节点互斥访问共享资源时需要分布式锁，常见实现基于 Redis（`SET NX EX` + 唯一值 + Lua 释放）或 etcd 的事务 API。其核心约束是：锁必须有超时，持有者必须能证明身份，防止误删他人的锁。

#### 3. 共识算法（Raft / Paxos）

共识协议让多个节点就一系列值的顺序达成一致。Raft 通过领导者选举、日志复制和安全性约束实现可理解的共识。etcd 是 Go 实现的 Raft 参考（其 `raft` 库可直接作为库嵌入 Go 应用），适合作为深入学习的第一手材料。

#### 4. 一致性哈希与数据分片

一致性哈希将键空间映射到环形哈希空间，节点增减时只影响相邻区间的数据。Go 的 map + 排序切片即可实现一个简洁的一致性哈希环：

```go
package main

import (
	"fmt"
	"hash/fnv"
	"sort"
)

// ConsistentHash 一致性哈希环
type ConsistentHash struct {
	nodes  []uint32 // 虚拟节点的哈希值（有序）
	nodeOf map[uint32]string
}

func NewConsistentHash() *ConsistentHash {
	return &ConsistentHash{nodeOf: make(map[uint32]string)}
}

func hash32(s string) uint32 {
	h := fnv.New32a()
	h.Write([]byte(s))
	return h.Sum32()
}

// Add 添加节点（带虚拟节点，默认 100 个）
func (c *ConsistentHash) Add(node string) {
	for i := 0; i < 100; i++ {
		h := hash32(fmt.Sprintf("%s#%d", node, i))
		c.nodes = append(c.nodes, h)
		c.nodeOf[h] = node
	}
	sort.Slice(c.nodes, func(i, j int) bool { return c.nodes[i] < c.nodes[j] })
}

// Get 返回 key 应归属的节点：找环上顺时针第一个大于等于 key 哈希的节点
func (c *ConsistentHash) Get(key string) string {
	h := hash32(key)
	idx := sort.Search(len(c.nodes), func(i int) bool { return c.nodes[i] >= h })
	if idx == len(c.nodes) {
		idx = 0 // 环回起点
	}
	return c.nodeOf[c.nodes[idx]]
}

func main() {
	ring := NewConsistentHash()
	ring.Add("node-a")
	ring.Add("node-b")
	ring.Add("node-c")

	for _, key := range []string{"user:1", "user:2", "order:42", "session:abc"} {
		fmt.Printf("%-12s -> %s\n", key, ring.Get(key))
	}
}
```

#### 5. 服务发现与注册

服务实例启动时向注册中心注册自身地址，消费方从注册中心拉取或订阅可用实例列表。etcd 的 `clientv3` 提供 lease（租约）+ keepalive 机制：实例心跳续租，宕机后租约到期自动从注册表中消失。

#### 6. 幂等性与重试

跨网络调用都可能失败，客户端重试要求服务端操作幂等。常用手段是请求唯一 ID + 去重表，以及指数退避重试：

```go
// retry 用指数退避重试 f，直到成功或达到次数上限
func retry(attempts int, base time.Duration, f func() error) error {
	var err error
	for i := 0; i < attempts; i++ {
		if err = f(); err == nil {
			return nil
		}
		time.Sleep(base * time.Duration(1<<i)) // 100ms, 200ms, 400ms...
	}
	return err
}
```

### Go 生态中的分布式基础组件

| 组件 | 用途 |
| ---- | ---- |
| etcd | 分布式键值存储，服务发现、配置中心、分布式锁、Raft 共识 |
| gRPC + protobuf | 高性能跨语言 RPC，服务间通信的事实标准 |
| go-micro / kratos | 微服务框架，集成服务发现、熔断、链路追踪 |
| NATS / Kafka | 分布式消息系统（见中间件章节） |
| gossip 库（hashicorp/memberlist） | 去中心化的节点成员管理与故障检测 |

### 总结

分布式系统的难点不在于单个算法，而在于把"网络不可靠、节点会挂、时钟不同步"这些事实纳入每一次设计决策。Go 的 goroutine + channel 让并发服务逻辑的编写变得简单，`net`、`net/rpc`、`gRPC` 提供了扎实的通信基础，而 etcd、Kubernetes 等生产级开源项目则是学习分布式工程实践的最佳教材。
