### Redis Bitmap

A Redis Bitmap is a special data structure that uses the bits of each byte in a string to store binary information. Bitmaps are usually used for large-scale boolean data such as user check-ins, event records and status flags. Although a Redis bitmap is essentially an extension of the string type, it provides a set of specific bit operations.

#### Scenario examples

1. **User check-in**
   - Example: record a user's check-in status for each day.
     ```bash
     SETBIT user:123:sign 1 1
     SETBIT user:123:sign 2 1
     GETBIT user:123:sign 1
     GETBIT user:123:sign 2
     ```
   - Note: use `SETBIT` to set the check-in status, and `GETBIT` to read it. Each bit in the bitmap represents the check-in status for a day.

2. **Active user statistics**
   - Example: record which users are active.
     ```bash
     SETBIT active_users 1 1
     SETBIT active_users 2 1
     BITCOUNT active_users
     ```
   - Note: use `SETBIT` to set a user's active status, and `BITCOUNT` to count the active users.

3. **Permission management**
   - Example: use a bitmap to represent user permissions.
     ```bash
     SETBIT user:123:permissions 0 1  # permission 0
     SETBIT user:123:permissions 1 0  # permission 1
     BITFIELD user:123:permissions GET u8 0
     BITFIELD user:123:permissions GET u8 1
     ```
   - Note: use `SETBIT` to set permissions, and `BITFIELD` to read permission information.

4. **Vote-flooding prevention**
   - Example: stop users from voting more than once.
     ```bash
     SETBIT votes 12345 1  # set the voting status of user ID 12345
     GETBIT votes 12345
     ```
   - Note: use `SETBIT` to set a user's voting status, and `GETBIT` to check whether the user has already voted.

5. **Monitoring flags**
   - Example: record the health status of machines.
     ```bash
     SETBIT machine_health 0 1  # machine healthy
     SETBIT machine_health 1 0  # machine failed
     BITPOS machine_health 1
     ```
   - Note: use `SETBIT` to set a machine's health status, and `BITPOS` to find the position of the first healthy machine.

#### Underlying implementation

A Redis bitmap is really bit operations on a string, and under the hood it relies on Redis's byte storage for strings. Every bitmap operation is performed by reading and writing the bits of the string's bytes.

1. **Memory layout of a bitmap**
   - A bitmap stores its data inside a Redis string, and each byte (8 bits) represents a group of boolean values. For example, a bitmap of length 1 can represent 8 boolean values.
   - The internal data structure of a bitmap (in bytes) is:
     ```c
     typedef struct bitmap {
         unsigned char *bits;   // the bitmap's byte array
         size_t length;         // length of the bitmap (in bits)
     } bitmap;
     ```

2. **Bitmap operations**
   - **SETBIT**: set the bit at a given offset to 1 or 0.
     ```c
     void setbit(bitmap *bm, size_t offset, int value) {
         size_t byteIndex = offset / 8;
         size_t bitIndex = offset % 8;
         if (value) {
             bm->bits[byteIndex] |= (1 << bitIndex);
         } else {
             bm->bits[byteIndex] &= ~(1 << bitIndex);
         }
     }
     ```
   - **GETBIT**: get the value of the bit at a given offset.
     ```c
     int getbit(bitmap *bm, size_t offset) {
         size_t byteIndex = offset / 8;
         size_t bitIndex = offset % 8;
         return (bm->bits[byteIndex] >> bitIndex) & 1;
     }
     ```
   - **BITCOUNT**: count the number of bits set to 1 in the bitmap.
     ```c
     size_t bitcount(bitmap *bm) {
         size_t count = 0;
         for (size_t i = 0; i < bm->length / 8; i++) {
             count += __builtin_popcount(bm->bits[i]);
         }
         return count;
     }
     ```
   - **BITPOS**: find the offset of the first bit set to 1 in the bitmap.
     ```c
     size_t bitpos(bitmap *bm, int value) {
         for (size_t i = 0; i < bm->length / 8; i++) {
             if (value == 1) {
                 if (bm->bits[i] != 0) {
                     return (i * 8) + __builtin_ctz(bm->bits[i]);
                 }
             } else {
                 if (bm->bits[i] != 0xFF) {
                     return (i * 8) + __builtin_ctz(~bm->bits[i]);
                 }
             }
         }
         return -1;
     }
     ```

A bitmap stores boolean data bit by bit inside a string, which is why it is the most memory-efficient choice for large-scale boolean flags such as check-ins and active-user statistics.

#### Using Redis Bitmaps in Go

In Go, you can use the `go-redis` library to work with Redis bitmaps. Here are some basic operations.

1. **Connect to Redis**
   ```go
   package main

   import (
       "context"
       "fmt"

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

2. **Set a bit**
   ```go
   func example(rdb *redis.Client) {
       err := rdb.SetBit(ctx, "bitmap", 10, 1).Err()
       if err != nil {
           panic(err)
       }
   }
   ```

3. **Get a bit**
   ```go
   func example(rdb *redis.Client) {
       bit, err := rdb.GetBit(ctx, "bitmap", 10).Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Bit value:", bit)
   }
   ```

4. **Count bits**
   ```go
   func example(rdb *redis.Client) {
       count, err := rdb.BitCount(ctx, "bitmap", nil).Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Bit count:", count)
   }
   ```

5. **Find a bit**
   ```go
   func example(rdb *redis.Client) {
       pos, err := rdb.BitPos(ctx, "bitmap", 1).Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("First set bit position:", pos)
   }
   ```

Boolean flags are stored bit by bit and operated on bit by bit, which is why bitmaps are the go-to choice for use cases like check-ins and active-user statistics.

## References

- [Redis Official Command Manual](https://redis.io/commands/)
- [go-redis Official Client](https://github.com/redis/go-redis)
- [go-redis · pkg.go.dev](https://pkg.go.dev/github.com/redis/go-redis/v9)

## Sibling pages

- [Geospatial](/redis/Geospatial.md)
- [Hash](/redis/Hash.md)
- [HyperLogLog](/redis/HyperLogLog.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Geospatial](/redis/Geospatial.md)
- [Hash](/redis/Hash.md)
- [HyperLogLog](/redis/HyperLogLog.md)
- [Install](/redis/Install.md)
- [List](/redis/List.md)
- [Readme](/redis/Readme.md)
- [Set](/redis/Set.md)
- [SortedSet](/redis/SortedSet.md)
- [Streams](/redis/Streams.md)
- [String](/redis/String.md)
