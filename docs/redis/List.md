### Redis Lists

A Redis list is a doubly linked list, used to store a sequence of ordered elements. The list type supports inserting and deleting elements from both ends, and suits scenarios like message queues, task scheduling, and leaderboards.

#### Scenarios

1. **Message queue**
   - Example:
     ```bash
     LPUSH queue "message1"
     LPUSH queue "message2"
     RPOP queue
     ```
   - Note: Uses `LPUSH` to push a message from the left, and `RPOP` to pop a message from the right, implementing a first-in-first-out (FIFO) message queue.

2. **Task scheduling**
   - Example:
     ```bash
     RPUSH tasks "task1"
     RPUSH tasks "task2"
     LPOP tasks
     ```
   - Note: Uses `RPUSH` to push a task from the right, and `LPOP` to pop a task from the left, implementing first-in-first-out (FIFO) task scheduling.

3. **Leaderboard**
   - Example:
     ```bash
     RPUSH leaderboard "user1"
     RPUSH leaderboard "user2"
     LRANGE leaderboard 0 -1
     ```
   - Note: Uses `RPUSH` to insert users, and `LRANGE` to get all users, implementing a simple leaderboard.

4. **Chat history**
   - Example:
     ```bash
     RPUSH chat:room1 "Hello!"
     RPUSH chat:room1 "Hi there!"
     LRANGE chat:room1 0 -1
     ```
   - Note: Uses `RPUSH` to insert chat messages, and `LRANGE` to get all the chat history.

5. **Fixed-length list**
   - Example:
     ```bash
     LPUSH log "error1"
     LPUSH log "error2"
     LTRIM log 0 99
     ```
   - Note: Uses `LPUSH` to insert log entries, and `LTRIM` to keep the list length at or below 100.

6. **Blocking queue**
   - Example:
     ```bash
     BRPOP queue 0
     ```
   - Note: Uses the `BRPOP` command to pop an element from the right; if the list is empty it blocks until a new element is pushed.

#### Underlying implementation

The underlying implementation of the Redis list type uses two data structures: `ziplist` and `linkedlist` (doubly linked list).

1. **Ziplist**
   - When a list has few elements and each element is short, Redis stores the list in a ziplist. A ziplist is a contiguous memory block that saves space.
   - Structure:
     ```c
     struct {
         unsigned int zlbytes;     // total bytes of the ziplist
         unsigned int zltail;      // offset to reach the tail of the list
         unsigned int zllen;       // number of nodes in the ziplist
         unsigned char entries[];  // data nodes
     };
     ```
   - Advantages: compact memory layout, suited to storing small amounts of data.

2. **Doubly linked list (linkedlist)**
   - When a list has many elements or some elements are long, Redis stores the list in a doubly linked list. A doubly linked list provides efficient insertion and deletion operations.
   - Structure:
     ```c
     typedef struct listNode {
         struct listNode *prev;    // pointer to previous node
         struct listNode *next;    // pointer to next node
         void *value;              // node value
     } listNode;
     
     typedef struct list {
         listNode *head;           // pointer to head node
         listNode *tail;           // pointer to tail node
         unsigned long len;        // number of nodes
         // ...
     } list;
     ```
   - Advantages: handles large amounts of data and long strings efficiently.

Redis picks the most suitable data structure for storing list data by trading off memory use against access speed. It starts by storing small lists in a ziplist, and once the list grows to a certain size it automatically converts to a doubly linked list, balancing space efficiency and performance.

#### Using Redis Lists in Go

In Go, you can use the `go-redis` library to work with Redis lists. Here are some basic operation examples.

1. **Connecting to Redis**
   ```go
   package main

   import (
       "context"

       "github.com/go-redis/redis/v8"
   )

   var ctx = context.Background()

   func main() {
       rdb := redis.NewClient(&redis.Options{
           Addr:     "localhost:6379",
           Password: "", // no password set
           DB:       0,  // use default DB
       })

       // call the example code
       example(rdb)
   }

   func example(rdb *redis.Client) {
       // example operations
   }
   ```

2. **Pushing elements**
   ```go
   func example(rdb *redis.Client) {
       err := rdb.LPush(ctx, "queue", "message1").Err()
       if err != nil {
           panic(err)
       }
       err = rdb.RPush(ctx, "queue", "message2").Err()
       if err != nil {
           panic(err)
       }
   }
   ```

3. **Popping elements**
   ```go
   func example(rdb *redis.Client) {
       msg, err := rdb.RPop(ctx, "queue").Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Popped message:", msg)
   }
   ```

4. **Getting elements in a range**
   ```go
   func example(rdb *redis.Client) {
       msgs, err := rdb.LRange(ctx, "queue", 0, -1).Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("All messages:", msgs)
   }
   ```

5. **Blocking pop**
   ```go
   func example(rdb *redis.Client) {
       msg, err := rdb.BRPop(ctx, 0, "queue").Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Popped message:", msg)
   }
   ```

Put these snippets together and you have the Go version of the scenarios above: `LPush`/`RPush` to enqueue, `RPop`/`LRange` to read, and `BRPop` to block waiting for a new element to arrive in the queue.

## References

- [Redis Official Command Manual](https://redis.io/commands/)
- [go-redis Official Client](https://github.com/redis/go-redis)
- [go-redis · pkg.go.dev](https://pkg.go.dev/github.com/redis/go-redis/v9)


## Sibling pages

- [Bitmap](/redis/Bitmap.md)
- [Geospatial](/redis/Geospatial.md)
- [Hash](/redis/Hash.md)
- [Install](/redis/Install.md)
- [Readme](/redis/Readme.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Install](/redis/Install.md)
- [Readme](/redis/Readme.md)
