### Redis Sets

A Redis set is an unordered collection of strings in which every element is unique and duplicates are not allowed. Sets suit scenarios that need fast lookups and deduplication, such as tag systems, friend lists, and recommendation systems.

#### Scenarios

1. **Tag system**
   - Example:
     ```bash
     SADD tags "golang"
     SADD tags "redis"
     SADD tags "database"
     SMEMBERS tags
     ```
   - Note: Uses `SADD` to add tags, and `SMEMBERS` to get all tags.

2. **Friend list**
   - Example:
     ```bash
     SADD friends:user1 "user2"
     SADD friends:user1 "user3"
     SADD friends:user2 "user1"
     SADD friends:user2 "user3"
     SINTER friends:user1 friends:user2
     ```
   - Note: Uses `SADD` to add friends, and `SINTER` to get mutual friends.

3. **Recommendation system**
   - Example:
     ```bash
     SADD viewed:product1 "user1"
     SADD viewed:product1 "user2"
     SADD viewed:product2 "user2"
     SADD viewed:product2 "user3"
     SUNION viewed:product1 viewed:product2
     ```
   - Note: Uses `SADD` to record users who viewed a product, and `SUNION` to get all users who have viewed any of some products.

4. **Deduplication**
   - Example:
     ```bash
     SADD unique:emails "user1@example.com"
     SADD unique:emails "user2@example.com"
     SADD unique:emails "user1@example.com"
     SMEMBERS unique:emails
     ```
   - Note: Uses `SADD` to add email addresses, and `SMEMBERS` to get the list of unique addresses.

5. **Randomly getting an element**
   - Example:
     ```bash
     SADD colors "red" "green" "blue"
     SRANDMEMBER colors
     ```
   - Note: Uses `SADD` to add colors, and `SRANDMEMBER` to randomly get a color.

#### Underlying implementation

The underlying implementation of Redis sets mainly uses two data structures: `intset` (integer set) and `hashtable`.

1. **Integer set (intset)**
   - When all elements of a set are integers and there are only a few of them, Redis stores the set in an integer set. An integer set is a compact encoding that saves memory.
   - Structure:
     ```c
     typedef struct intset {
         uint32_t encoding;        // encoding method
         uint32_t length;          // number of elements in the set
         int8_t contents[];        // element array
     } intset;
     ```
   - Advantages: small memory footprint, suited to storing small integer sets.

2. **Hashtable**
   - When the set's elements are complex types or there are many of them, Redis stores the set in a hashtable. A hashtable provides fast lookup, insertion, and deletion operations.
   - Structure:
     ```c
     typedef struct dictht {
         dictEntry **table;        // hashtable array
         unsigned long size;       // hashtable size
         unsigned long sizemask;   // hashtable size mask, used to compute the index
         unsigned long used;       // number of nodes in use
     } dictht;
     
     typedef struct dictEntry {
         void *key;                // key
         void *val;                // value (NULL in a set)
         struct dictEntry *next;   // linked-list pointer, resolves collisions
     } dictEntry;
     ```
   - Advantages: handles large amounts of data efficiently, with fast lookups.

Redis dynamically picks the most suitable data structure for storage based on the set's element type and count, striking a balance between performance and memory use.

#### Using Redis Sets in Go

In Go, you can use the `go-redis` library to work with Redis sets. Here are some basic operation examples.

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

2. **Adding elements**
   ```go
   func example(rdb *redis.Client) {
       err := rdb.SAdd(ctx, "tags", "golang").Err()
       if err != nil {
           panic(err)
       }
       err = rdb.SAdd(ctx, "tags", "redis").Err()
       if err != nil {
           panic(err)
       }
   }
   ```

3. **Getting all elements**
   ```go
   func example(rdb *redis.Client) {
       members, err := rdb.SMembers(ctx, "tags").Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Tags:", members)
   }
   ```

4. **Checking whether an element exists**
   ```go
   func example(rdb *redis.Client) {
       exists, err := rdb.SIsMember(ctx, "tags", "golang").Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Is 'golang' a member of tags?", exists)
   }
   ```

5. **Deleting elements**
   ```go
   func example(rdb *redis.Client) {
       err := rdb.SRem(ctx, "tags", "redis").Err()
       if err != nil {
           panic(err)
       }
       members, err := rdb.SMembers(ctx, "tags").Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Tags after removal:", members)
   }
   ```

6. **Randomly getting an element**
   ```go
   func example(rdb *redis.Client) {
       member, err := rdb.SRandMember(ctx, "tags").Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Random tag:", member)
   }
   ```

The set API in `go-redis` maps one-to-one onto the Redis commands: `SAdd`/`SMembers`/`SIsMember`/`SRem`/`SRandMember` correspond to `SADD`/`SMEMBERS`/`SISMEMBER`/`SREM`/`SRANDMEMBER`, so once you know the command names, the library comes along for the ride.

## References

- [Redis Official Command Manual](https://redis.io/commands/)
- [go-redis Official Client](https://github.com/redis/go-redis)
- [go-redis · pkg.go.dev](https://pkg.go.dev/github.com/redis/go-redis/v9)


## Sibling pages

- [Bitmap](/redis/Bitmap.md)
- [Geospatial](/redis/Geospatial.md)
- [Hash](/redis/Hash.md)
- [Readme](/redis/Readme.md)
- [SortedSet](/redis/SortedSet.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Readme](/redis/Readme.md)
- [SortedSet](/redis/SortedSet.md)
