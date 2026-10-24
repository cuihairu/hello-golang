# Sliding Window

The sliding window is a core concept in network transmission and flow control, and it is also a widely used rate-limiting algorithm. This page records the TCP sliding window mechanism separately from how a rate limiter is built on the sliding window in Go.

### Sliding Window in TCP

TCP uses the sliding window for flow control and reliable transmission:

- **Send window**: the sender maintains a window; bytes inside it can be sent continuously without waiting for an individual ACK on each one. The left edge advances as the receiver acknowledges bytes, and the right edge is set by the receive window (rwnd) advertised by the peer.
- **Receive window**: the receiver tells the sender how much more data it can accept via the window field in the TCP header, so the sender does not flood the receiver's buffer.
- **Sliding**: once an ACK arrives the window "slides" forward, and new data enters the window and can be sent. Window size = min(rwnd, cwnd) (the smaller of the receive window and the congestion window).

```
Acknowledged  [ Sendable but unacked | Not sent ]     Not sendable
Sent <-------+----------------------------+----> Sequence space
                <------ Send window ------>
                 Window slides right with each ACK
```

### Application Layer: Sliding Window Rate Limiter

As a rate-limiting algorithm, the sliding window avoids the "boundary spike" problem of a fixed window counter: count the requests in the last N seconds and reject them once the threshold is exceeded.

The implementation below stores the timestamp of each request in the window in a circular queue (ring buffer). Each check first evicts expired records, then sees whether there is room; the queue length is fixed at `limit`:

```go
package main

import (
	"fmt"
	"sync"
	"time"
)

// SlidingWindowLimiter is a rate limiter based on the sliding window:
// it allows at most limit requests within window time
type SlidingWindowLimiter struct {
	mu      sync.Mutex
	limit   int           // max requests allowed within the window
	window  time.Duration // window length
	stamps  []time.Time   // circular queue storing timestamps of requests in the window
	head    int           // head index of the queue
	count   int           // number of valid elements in the queue
}

func NewSlidingWindowLimiter(limit int, window time.Duration) *SlidingWindowLimiter {
	return &SlidingWindowLimiter{
		limit:  limit,
		window: window,
		stamps: make([]time.Time, limit),
	}
}

// Allow checks whether the current request is permitted
func (l *SlidingWindowLimiter) Allow() bool {
	now := time.Now()
	l.mu.Lock()
	defer l.mu.Unlock()

	// evict expired requests that have fallen outside the window
	for l.count > 0 && now.Sub(l.stamps[l.head]) >= l.window {
		l.head = (l.head + 1) % len(l.stamps)
		l.count--
	}

	if l.count >= l.limit {
		return false // window is full, reject
	}

	// record this request (queue is not full, so the tail slot must be empty)
	tail := (l.head + l.count) % len(l.stamps)
	l.stamps[tail] = now
	l.count++
	return true
}

func main() {
	// allow at most 5 requests within 1 second
	limiter := NewSlidingWindowLimiter(5, time.Second)

	for i := 1; i <= 8; i++ {
		if limiter.Allow() {
			fmt.Printf("Request %d: allowed\n", i)
		} else {
			fmt.Printf("Request %d: rate-limited\n", i)
		}
		time.Sleep(100 * time.Millisecond)
	}

	// wait for the window to slide past so requests are allowed again
	time.Sleep(800 * time.Millisecond)
	fmt.Println("After the window slides past:")
	if limiter.Allow() {
		fmt.Println("Request 9: allowed")
	}
}
```

Sample output:

```
Request 1: allowed
Request 2: allowed
Request 3: allowed
Request 4: allowed
Request 5: allowed
Request 6: rate-limited
Request 7: rate-limited
Request 8: rate-limited
After the window slides past:
Request 9: allowed
```

### Comparison with Other Rate Limiting Algorithms

| Algorithm | Characteristics | Drawbacks |
| ---- | ---- | ---- |
| Fixed window counter | Simplest to implement | May see 2x burst traffic at window boundaries |
| Sliding window log (implemented in this section) | Precise, no boundary spikes | Records every request; high memory overhead at high concurrency |
| Sliding window counter | Splits the window into small buckets to approximate sliding; low memory overhead | Accuracy depends on the number of buckets |
| Token bucket | Allows some burst; smooths the average rate | Needs background token generation or lazy computation |

### Summary

TCP's sliding window solves "how fast is it right to send," while the application-layer sliding window limiter solves "how many requests are allowed per unit time." Their shared idea is to measure recent behaviour with an interval that slides forward over time, rather than looking at each moment in isolation. In Go services, the sliding window limiter is commonly used for API gateways, middleware, and client retry control.

## References

- [net standard library](https://pkg.go.dev/net)
- [net/http standard library](https://pkg.go.dev/net/http)
- [RFC 9293 · Transmission Control Protocol (TCP, replaces RFC 793)](https://www.rfc-editor.org/rfc/rfc9293)


## Sibling pages

- [Advanced](/net/Advanced.md)
- [Concurrence](/net/Concurrence.md)
- [Intro](/net/Intro.md)
- [Proto](/net/Proto.md)
- [Socket](/net/Socket.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Proto](/net/Proto.md)
- [Socket](/net/Socket.md)
