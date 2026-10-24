### Redis Hashes

A Redis hash is a collection of key-value pairs: one key holds multiple fields and their values, which suits objects with several attributes, like user information.

#### Scenarios

1. **Storing and retrieving user information**
   - Example:
     ```bash
     HSET user:1000 name "Alice" age "30" email "alice@example.com"
     HGETALL user:1000
     ```
   - Note: Uses the `HSET` command to store user information, and `HGETALL` to get all fields and values.

2. **Updating a specific field**
   - Example:
     ```bash
     HSET user:1000 age "31"
     HGET user:1000 age
     ```
   - Note: Uses `HSET` to update the user's age, and `HGET` to get the value of a specific field.

3. **Deleting a field**
   - Example:
     ```bash
     HDEL user:1000 email
     HGETALL user:1000
     ```
   - Note: Uses `HDEL` to delete the user's email field, and `HGETALL` to get all fields and values.

4. **Checking field existence**
   - Example:
     ```bash
     HEXISTS user:1000 email
     ```
   - Note: Uses `HEXISTS` to check whether a field exists.

5. **Getting all fields**
   - Example:
     ```bash
     HKEYS user:1000
     ```
   - Note: Uses `HKEYS` to get all field names.

6. **Getting all values**
   - Example:
     ```bash
     HVALS user:1000
     ```
   - Note: Uses `HVALS` to get the values of all fields.

7. **Incrementing a field value**
   - Example:
     ```bash
     HINCRBY user:1000 age 1
     HGET user:1000 age
     ```
   - Note: Uses `HINCRBY` to increment a field's numeric value, and `HGET` to get the field's value.

#### Underlying implementation

The underlying implementation of Redis hashes mainly uses two data structures: `ziplist` and `hashtable`.

1. **Ziplist**
   - When a hash has few key-value pairs and each pair is short, Redis stores the hash in a ziplist. A ziplist is a specially encoded contiguous memory block that saves space.
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

2. **Hashtable**
   - When a hash has many key-value pairs or some pairs are long, Redis stores the hash in a hashtable. A hashtable provides fast lookup, insertion, and deletion operations.
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
         void *val;                // value
         struct dictEntry *next;   // linked-list pointer, resolves collisions
     } dictEntry;
     ```
   - Advantages: handles large amounts of data and long strings efficiently.

Redis picks the most suitable data structure for storing hash data by trading off memory use against access speed. It starts by storing small hashes in a ziplist, and once the hash grows to a certain size it automatically converts to a hashtable, balancing space efficiency and performance.

## References

- [Redis Official Command Manual](https://redis.io/commands/)
- [go-redis Official Client](https://github.com/redis/go-redis)
- [go-redis · pkg.go.dev](https://pkg.go.dev/github.com/redis/go-redis/v9)

## Sibling pages

- [Bitmap](/redis/Bitmap.md)
- [Geospatial](/redis/Geospatial.md)
- [HyperLogLog](/redis/HyperLogLog.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Bitmap](/redis/Bitmap.md)
- [Geospatial](/redis/Geospatial.md)
- [HyperLogLog](/redis/HyperLogLog.md)
- [Install](/redis/Install.md)
- [List](/redis/List.md)
- [Readme](/redis/Readme.md)
- [Set](/redis/Set.md)
- [SortedSet](/redis/SortedSet.md)
- [Streams](/redis/Streams.md)
- [String](/redis/String.md)
