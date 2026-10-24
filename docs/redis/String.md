### Redis Strings

The Redis string type is the most basic data type; it can store text, numbers, and binary data. Here are eight common scenarios, then the `SDS` underneath.

#### Scenarios

1. **Storing simple key-value pairs**
   - Example:
     ```bash
     SET key "value"
     GET key
     ```
   - Note: Sets the value of key `key` to `value`, then retrieves that value.

2. **Counters**
   - Example:
     ```bash
     INCR page_view_count
     GET page_view_count
     ```
   - Note: Increments the value of key `page_view_count` by 1, used to record page view counts.

3. **Storing binary data**
   - Example:
     ```bash
     SET image_data "\x89PNG..."
     GET image_data
     ```
   - Note: Can store binary data, such as images or files.

4. **Keys with an expiry**
   - Example:
     ```bash
     SET session_token "abc123" EX 3600
     GET session_token
     ```
   - Note: Sets the value of key `session_token` and sets its expiry to 3600 seconds.

5. **Batch operations**
   - Example:
     ```bash
     MSET key1 "value1" key2 "value2"
     MGET key1 key2
     ```
   - Note: Sets multiple key-value pairs in one call, then retrieves the values of multiple keys.

6. **String operations**
   - Example:
     ```bash
     APPEND key "suffix"
     GETRANGE key 0 4
     ```
   - Note: Appends the string `suffix` to the end of the value of `key`, and retrieves a partial value of `key`.

7. **Bit operations**
   - Example:
     ```bash
     SETBIT bitkey 7 1
     GETBIT bitkey 7
     BITCOUNT bitkey
     ```
   - Note: Uses bit operations to set, get, and count bits.

8. **Numeric operations**
   - Example:
     ```bash
     INCRBYFLOAT price 12.34
     DECR quantity
     ```
   - Note: Increments and decrements numeric values.

#### Underlying implementation

Underneath, Redis strings are `SDS` (Simple Dynamic String). It wraps a layer around a C `char` array, with the length and remaining space recorded in the header. Implementation traits of `SDS`:

1. **Dynamic expansion**:
   - `SDS` supports dynamic expansion; as the string grows it automatically allocates enough space, reducing the number of memory allocations.
   - Example code:
     ```c
     struct sdshdr {
         int len;       // used length
         int free;      // available space
         char buf[];    // data buffer
     };
     ```

2. **Binary safe**:
   - `SDS` can store any binary data, including the null byte, because it records the string length via the `len` property rather than being null-terminated.

3. **Pre-allocation**:
   - When expanding, `SDS` pre-allocates space, reducing the memory allocation cost of subsequent expansions.
   - Expansion rule: if the new length is below 1MB, allocate twice the new length; otherwise allocate an increment of 1MB.

4. **Compatible with C strings**:
   - `SDS` is compatible with C strings; a null byte is always kept at the end of `buf`, but it is not counted in `len`.

5. **Memory efficiency**:
   - Through sensible memory management and expansion strategy, `SDS` reduces memory fragmentation and improves memory utilization.

`SDS` keeps its own length, which sidesteps the buffer overflows and repeated allocations that plague C strings; pre-allocation also means operations like append and counting do fewer memory allocations. All eight scenarios above — storage, counting, concatenation, bit operations, numeric operations — sit on top of this layer.

## References

- [Redis Official Command Manual](https://redis.io/commands/)
- [go-redis Official Client](https://github.com/redis/go-redis)
- [go-redis · pkg.go.dev](https://pkg.go.dev/github.com/redis/go-redis/v9)


## Sibling pages

- [Bitmap](/redis/Bitmap.md)
- [Geospatial](/redis/Geospatial.md)
- [Hash](/redis/Hash.md)
- [Streams](/redis/Streams.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Streams](/redis/Streams.md)
