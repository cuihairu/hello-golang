# Distributed systems

A distributed system is one where multiple machines connected over a network work together to provide a service. etcd, Kubernetes, Consul, and TiKV are all written in Go: goroutines handle concurrency, and a single statically compiled binary deploys directly, which is why Go is a common choice for this kind of system. Here I round up the core problem areas of distributed systems and how Go is typically applied in them.

### The core problems a distributed system has to solve

1. **Unreliable networks**: messages between nodes may be delayed, reordered, or lost, so every call has to account for timeouts and retries.
2. **Partial failure**: when some nodes in the cluster go down, the system as a whole still has to be available, which is entirely different from a single-machine program's "either everything crashes or everything is fine."
3. **Clocks and ordering**: clocks on different machines are not in sync, so you cannot rely on global time to judge event order; you need a logical clock or a consensus protocol to establish a total order.
4. **Data consistency**: how multiple replicas keep their data consistent — strong consistency (linearizable), eventual consistency, or something in between.
5. **Scalability**: use data sharding and load balancing so the system can scale horizontally.

### Common distributed patterns and Go implementations

#### 1. Heartbeats and failure detection

Nodes report heartbeats on a schedule, and the monitor declares a node failed when it stops receiving heartbeats past a timeout. Go's `time.Ticker` and goroutines are naturally suited to this kind of periodic task:

```go
package main

import (
	"fmt"
	"sync"
	"time"
)

// NodeStatus records the last heartbeat time of each node
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
	status.Beat("node-1") // report one heartbeat first at startup

	// simulate node "node-1" sending a heartbeat every 100ms
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

	fmt.Println("node-1 alive:", status.Alive("node-1")) // true
	fmt.Println("node-2 alive:", status.Alive("node-2")) // false (never sent a heartbeat)

	time.Sleep(300 * time.Millisecond)
	close(stop)
	time.Sleep(300 * time.Millisecond)
	fmt.Println("node-1 alive after heartbeat stops:", status.Alive("node-1")) // false
}
```

#### 2. Distributed locks

When multiple nodes need mutual exclusion over a shared resource, a distributed lock is needed. Common implementations are based on Redis (`SET NX EX` + a unique value + a Lua script to release) or etcd's transaction API. The core constraints are: the lock must have a timeout, and the holder must be able to prove its identity, to prevent accidentally deleting someone else's lock.

#### 3. Consensus algorithms (Raft / Paxos)

A consensus protocol lets multiple nodes agree on the order of a sequence of values. Raft achieves understandable consensus through leader election, log replication, and safety constraints. etcd is a Go implementation of a Raft reference (its `raft` library can be embedded directly as a library in a Go application) and is first-hand material you can consult when studying its implementation.

#### 4. Consistent hashing and data sharding

Consistent hashing maps the keyspace onto a circular hash space, so adding or removing nodes only affects data in the adjacent intervals. A clean consistent hash ring can be implemented in Go with a map plus a sorted slice:

```go
package main

import (
	"fmt"
	"hash/fnv"
	"sort"
)

// ConsistentHash is a consistent hash ring
type ConsistentHash struct {
	nodes  []uint32 // hash values of virtual nodes (sorted)
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

// Add adds a node (with virtual nodes, 100 by default)
func (c *ConsistentHash) Add(node string) {
	for i := 0; i < 100; i++ {
		h := hash32(fmt.Sprintf("%s#%d", node, i))
		c.nodes = append(c.nodes, h)
		c.nodeOf[h] = node
	}
	sort.Slice(c.nodes, func(i, j int) bool { return c.nodes[i] < c.nodes[j] })
}

// Get returns the node a key belongs to: find the first node clockwise on the ring whose hash is >= the key's hash
func (c *ConsistentHash) Get(key string) string {
	h := hash32(key)
	idx := sort.Search(len(c.nodes), func(i int) bool { return c.nodes[i] >= h })
	if idx == len(c.nodes) {
		idx = 0 // wrap around to the start
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

#### 5. Service discovery and registration

When a service instance starts up, it registers its own address with a registry; consumers pull or subscribe to the list of available instances from the registry. etcd's `clientv3` provides a lease + keepalive mechanism: instances renew their lease via heartbeats, and after a crash the lease expires and the instance automatically disappears from the registry.

#### 6. Idempotency and retries

Cross-network calls can fail, so client retries require the server-side operation to be idempotent. Common techniques are a request-unique ID plus a dedup table, and exponential backoff retries:

```go
// retry retries f with exponential backoff until it succeeds or the attempt limit is reached
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

### Distributed building blocks in the Go ecosystem

| Component | Purpose |
| ---- | ---- |
| etcd | distributed key-value store: service discovery, configuration center, distributed locks, Raft consensus |
| gRPC + protobuf | high-performance cross-language RPC, the de facto standard for inter-service communication |
| go-micro / kratos | microservice frameworks, integrating service discovery, circuit breaking, and tracing |
| NATS / Kafka | distributed message systems (see the middleware chapter) |
| gossip libraries (hashicorp/memberlist) | decentralized node membership management and failure detection |

### Summary

Every design decision in a distributed system has to start by accepting three facts: the network delays and drops packets, nodes crash, and clocks are out of sync — heartbeat detection, idempotent retries, and consensus protocols all aim at exactly those. On the Go side, goroutines plus channels write the concurrent service logic, while `net`, `net/rpc`, and `gRPC` provide the communication foundation. You can see these practices fully landed in the source of etcd and Kubernetes.

## References

- [Official blog · Perfectly Reproducible, Verified Go Toolchains](https://go.dev/blog/rebuild)
- [Official · Go Modules user guide](https://go.dev/doc/modules/)

## Sibling pages

- [Mod](/mod/Mod.md)
- [Work](/mod/Work.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Mod](/mod/Mod.md)
