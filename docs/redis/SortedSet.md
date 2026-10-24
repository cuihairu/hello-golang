### Redis Sorted Set

A Redis Sorted Set is a set of strings with a score attached to each member. Every member has a unique score, and Redis sorts them by that score. It fits cases like leaderboards and delay queues.

#### Scenario examples

1. **Leaderboard**
   - Example:
     ```bash
     ZADD leaderboard 100 "user1"
     ZADD leaderboard 200 "user2"
     ZADD leaderboard 150 "user3"
     ZRANGE leaderboard 0 -1 WITHSCORES
     ```
   - Note: use `ZADD` to add users and their scores, and `ZRANGE` to read the leaderboard.

2. **Delay queue**
   - Example:
     ```bash
     ZADD delay_queue 1627474800 "task1"
     ZADD delay_queue 1627478400 "task2"
     ZRANGEBYSCORE delay_queue -inf 1627478400
     ```
   - Note: use `ZADD` to add tasks and their execution times, and `ZRANGEBYSCORE` to read tasks that are due.

3. **Event scheduling**
   - Example:
     ```bash
     ZADD schedule 1627474800 "event1"
     ZADD schedule 1627478400 "event2"
     ZRANGEBYSCORE schedule -inf +inf
     ```
   - Note: use `ZADD` to add events and their times, and `ZRANGEBYSCORE` to read all events.

4. **Rank query**
   - Example:
     ```bash
     ZADD scores 90 "Alice"
     ZADD scores 80 "Bob"
     ZADD scores 95 "Charlie"
     ZRANK scores "Alice"
     ```
   - Note: use `ZADD` to add users and their scores, and `ZRANK` to get a user's rank.

5. **Range query**
   - Example:
     ```bash
     ZADD temperatures 20 "New York"
     ZADD temperatures 25 "Los Angeles"
     ZADD temperatures 15 "Chicago"
     ZRANGEBYSCORE temperatures 15 25
     ```
   - Note: use `ZADD` to add cities and their temperatures, and `ZRANGEBYSCORE` to read cities within a given range.

#### Underlying implementation

The underlying implementation of a Redis Sorted Set is based on two data structures: `ziplist` and `skiplist`.

1. **Ziplist**
   - When a sorted set has few elements and each element is short, Redis stores it in a ziplist. A ziplist is a compact in-memory structure that stores small amounts of data efficiently.
   - Structure:
     ```c
     struct {
         unsigned int zlbytes;     // total bytes of the ziplist
         unsigned int zltail;      // offset to the tail
         unsigned int zllen;       // number of nodes in the ziplist
         unsigned char entries[];  // data nodes
     };
     ```
   - Advantages: small memory footprint, well suited to small sorted sets.

2. **Skiplist**
   - When a sorted set has many elements or each element is long, Redis stores it in a skiplist. A skiplist is an efficient ordered data structure that supports fast insertion, deletion and lookup.
   - Structure:
     ```c
     typedef struct zskiplistNode {
         sds ele;                           // element
         double score;                      // score
         struct zskiplistNode *backward;    // backward pointer
         struct zskiplistLevel {
             struct zskiplistNode *forward; // forward pointer
             unsigned int span;             // span
         } level[];
     } zskiplistNode;

     typedef struct zskiplist {
         struct zskiplistNode *header;      // head node
         struct zskiplistNode *tail;        // tail node
         unsigned long length;              // length
         int level;                         // number of levels
     } zskiplist;
     ```
   - Advantages: handles large datasets efficiently, with fast lookups.

Redis picks the most suitable data structure dynamically, based on the number of elements and the length of each element, to balance performance against memory use.

#### Using Redis Sorted Sets in Go

In Go, the `go-redis` library provides methods for working with sorted sets.

1. **Connect to Redis**
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

2. **Add elements**
   ```go
   func example(rdb *redis.Client) {
       err := rdb.ZAdd(ctx, "leaderboard", &redis.Z{
           Score:  100,
           Member: "user1",
       }).Err()
       if err != nil {
           panic(err)
       }
       err = rdb.ZAdd(ctx, "leaderboard", &redis.Z{
           Score:  200,
           Member: "user2",
       }).Err()
       if err != nil {
           panic(err)
       }
   }
   ```

3. **Get all elements**
   ```go
   func example(rdb *redis.Client) {
       members, err := rdb.ZRangeWithScores(ctx, "leaderboard", 0, -1).Result()
       if err != nil {
           panic(err)
       }
       for _, member := range members {
           fmt.Printf("Member: %s, Score: %f\n", member.Member, member.Score)
       }
   }
   ```

4. **Check whether an element exists**
   ```go
   func example(rdb *redis.Client) {
       score, err := rdb.ZScore(ctx, "leaderboard", "user1").Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Score of 'user1':", score)
   }
   ```

5. **Delete an element**
   ```go
   func example(rdb *redis.Client) {
       err := rdb.ZRem(ctx, "leaderboard", "user1").Err()
       if err != nil {
           panic(err)
       }
       members, err := rdb.ZRangeWithScores(ctx, "leaderboard", 0, -1).Result()
       if err != nil {
           panic(err)
       }
       for _, member := range members {
           fmt.Printf("Member: %s, Score: %f\n", member.Member, member.Score)
       }
   }
   ```

6. **Range query**
   ```go
   func example(rdb *redis.Client) {
       members, err := rdb.ZRangeByScoreWithScores(ctx, "leaderboard", &redis.ZRangeBy{
           Min: "150",
           Max: "200",
       }).Result()
       if err != nil {
           panic(err)
       }
       for _, member := range members {
           fmt.Printf("Member: %s, Score: %f\n", member.Member, member.Score)
       }
   }
   ```

## References

- [Redis Official Command Manual](https://redis.io/commands/)
- [go-redis Official Client](https://github.com/redis/go-redis)
- [go-redis · pkg.go.dev](https://pkg.go.dev/github.com/redis/go-redis/v9)


## Sibling pages

- [Bitmap](/redis/Bitmap.md)
- [Geospatial](/redis/Geospatial.md)
- [Hash](/redis/Hash.md)
- [Set](/redis/Set.md)
- [Streams](/redis/Streams.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Set](/redis/Set.md)
- [Streams](/redis/Streams.md)
