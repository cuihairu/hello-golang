# Circular Buffer

A circular buffer (also called a ring buffer) is a fixed-size buffer in which data wraps around repeatedly. It suits scenarios that recycle the same chunk of space over and over, such as stream processing and task queues.

### Overview of the Circular Buffer

It consists of an array and two indexes: one marks the read position, the other the write position. When the write index reaches the end of the array it wraps back to the beginning, forming a "ring." Reads and writes therefore never have to move existing data.

### Basic Operations of the Circular Buffer

1. **Initialization**:
   - Create a fixed-size array as the buffer and initialize the read/write pointers.
   
   ```go
   type RingBuffer struct {
       buffer []byte
       size   int
       head   int
       tail   int
       count  int
   }

   func NewRingBuffer(size int) *RingBuffer {
       return &RingBuffer{
           buffer: make([]byte, size),
           size:   size,
           head:   0,
           tail:   0,
           count:  0,
       }
   }
   ```

2. **Writing data**:
   - Write data into the buffer. The write pointer wraps back to the beginning when it reaches the end of the array. When the buffer is full, only as much as the remaining space can hold is written, and the number of bytes actually written is returned.
   
   ```go
   func (rb *RingBuffer) Write(data []byte) int {
       n := len(data)
       if n > rb.size {
           n = rb.size
       }

       // compute how many bytes can be written
       if rb.count+len(data) > rb.size {
           n = rb.size - rb.count
       }

       // write the data
       for i := 0; i < n; i++ {
           rb.buffer[rb.tail] = data[i]
           rb.tail = (rb.tail + 1) % rb.size
           rb.count++
       }

       return n
   }
   ```

3. **Reading data**:
   - Read data from the buffer. The read pointer wraps back to the beginning when it reaches the end of the array.

   ```go
   func (rb *RingBuffer) Read(p []byte) int {
       n := len(p)
       if n > rb.count {
           n = rb.count
       }

       // read the data
       for i := 0; i < n; i++ {
           p[i] = rb.buffer[rb.head]
           rb.head = (rb.head + 1) % rb.size
           rb.count--
       }

       return n
   }
   ```

4. **Checking buffer state**:
   - Check whether the buffer is full, empty, and so on.

   ```go
   func (rb *RingBuffer) IsFull() bool {
       return rb.count == rb.size
   }

   func (rb *RingBuffer) IsEmpty() bool {
       return rb.count == 0
   }
   ```

### Application Scenarios

1. **Stream processing**:
   - In stream processing, a circular buffer handles continuous data streams, such as network packets and real-time sensor data.

2. **Task queues**:
   - In a producer-consumer model, a circular buffer can serve as a task queue that stores pending tasks.

3. **Audio/video processing**:
   - In audio and video data streams, a circular buffer caches data, ensuring the continuity and stability of the data.

### Advantages

The buffer size is fixed, so there is no dynamic allocation and no memory fragmentation throughout. Reads and writes only adjust indexes and never move data, with time complexity O(1). The same space is recycled in a loop, which means fewer copies than a sequential queue.

### Example Code

```go
package main

import (
    "fmt"
)

type RingBuffer struct {
    buffer []byte
    size   int
    head   int
    tail   int
    count  int
}

func NewRingBuffer(size int) *RingBuffer {
    return &RingBuffer{
        buffer: make([]byte, size),
        size:   size,
        head:   0,
        tail:   0,
        count:  0,
    }
}

func (rb *RingBuffer) Write(data []byte) int {
    n := len(data)
    if n > rb.size {
        n = rb.size
    }

    if rb.count+len(data) > rb.size {
        n = rb.size - rb.count
    }

    for i := 0; i < n; i++ {
        rb.buffer[rb.tail] = data[i]
        rb.tail = (rb.tail + 1) % rb.size
        rb.count++
    }

    return n
}

func (rb *RingBuffer) Read(p []byte) int {
    n := len(p)
    if n > rb.count {
        n = rb.count
    }

    for i := 0; i < n; i++ {
        p[i] = rb.buffer[rb.head]
        rb.head = (rb.head + 1) % rb.size
        rb.count--
    }

    return n
}

func (rb *RingBuffer) IsFull() bool {
    return rb.count == rb.size
}

func (rb *RingBuffer) IsEmpty() bool {
    return rb.count == 0
}

func main() {
    rb := NewRingBuffer(5)
    rb.Write([]byte("hello"))
    fmt.Println(rb.IsFull()) // true

    buf := make([]byte, 5)
    rb.Read(buf)
    fmt.Println(string(buf)) // "hello"

    rb.Write([]byte("world"))
    fmt.Println(rb.IsEmpty()) // false
}
```

`main` first writes 5 bytes to fill the buffer, so `IsFull` returns true; after reading it out it writes `world`, and `IsEmpty` returns false.

## References

- [Circular buffer · Wikipedia](https://en.wikipedia.org/wiki/Circular_buffer)

## Sibling pages

- [DynamicArray](/algo/array/DynamicArray.md)
- [Array](/algo/array/Array.md)
- [DoubleEndedQueue](/algo/array/DoubleEndedQueue.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Array](/algo/array/Array.md)
- [DoubleEndedQueue](/algo/array/DoubleEndedQueue.md)
- [MultidimensionalArray](/algo/array/MultidimensionalArray.md)
- [PriorityQueue](/algo/array/PriorityQueue.md)
- [SparseArray](/algo/array/SparseArray.md)
