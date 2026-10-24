### Redis HyperLogLog

Redis HyperLogLog is a structure for cardinality estimation: you put elements in, then use `PFCOUNT` to get an approximate value. It answers questions like "how many distinct elements are there" — counting unique visitors, unique IPs and so on. It trades a probabilistic algorithm for memory, storing a whole set in 12KB by default.

#### Scenario examples

1. **Website visitor statistics**
   - Example: count the number of unique visitors to a website.
     ```bash
     PFADD page_views "user123"
     PFADD page_views "user456"
     PFADD page_views "user123"  # add the same user again
     PFCOUNT page_views
     ```
   - Note: use `PFADD` to add users, and `PFCOUNT` to get the number of unique users.

2. **Social media follower counts**
   - Example: count the number of unique followers of an account.
     ```bash
     PFADD twitter_followers "user789"
     PFADD twitter_followers "user101"
     PFCOUNT twitter_followers
     ```
   - Note: use `PFADD` to add followers, and `PFCOUNT` to get the total number of followers.

3. **Unique event counting**
   - Example: count the number of unique occurrences of an event.
     ```bash
     PFADD unique_events "event1"
     PFADD unique_events "event2"
     PFADD unique_events "event1"  # add the same event again
     PFCOUNT unique_events
     ```
   - Note: use `PFADD` to record events, and `PFCOUNT` to get the number of unique occurrences.

4. **Log analysis**
   - Example: count the number of unique IP addresses in logs.
     ```bash
     PFADD log_ips "192.168.1.1"
     PFADD log_ips "192.168.1.2"
     PFCOUNT log_ips
     ```
   - Note: use `PFADD` to add IP addresses, and `PFCOUNT` to get the number of unique IPs.

5. **Ad click statistics**
   - Example: count the number of unique clicks on an ad.
     ```bash
     PFADD ad_clicks "click1"
     PFADD ad_clicks "click2"
     PFCOUNT ad_clicks
     ```
   - Note: use `PFADD` to add click records, and `PFCOUNT` to get the number of unique clicks.

#### Underlying implementation

Redis HyperLogLog can be broken down into four things:

1. **Probabilistic algorithm**
   - HyperLogLog uses a probabilistic algorithm to estimate the number of unique elements. The core of the algorithm maps elements into a fixed range of buckets through a random hash function, then uses the "maximum leading zeros" idea from statistics to estimate the cardinality.

2. **Data structure**
   - **Buckets**: HyperLogLog uses a fixed number of buckets, and each bucket stores the maximum length of the leading zeros among the elements mapped to it.
   - **Hash function**: elements are mapped into buckets through a hash function, and the length of the leading zeros in the hash value is used to estimate the number of unique elements.

3. **Memory usage**
   - HyperLogLog uses O(log log N) memory. Redis stores a HyperLogLog in 12KB of memory by default.

4. **Commands**
   - **PFADD**: add elements to a HyperLogLog.
     ```bash
     PFADD key element [element ...]
     ```
   - **PFCOUNT**: get the cardinality estimate of a HyperLogLog.
     ```bash
     PFCOUNT key [key ...]
     ```
   - **PFMERGE**: merge multiple HyperLogLog data structures.
     ```bash
     PFMERGE destkey sourcekey [sourcekey ...]
     ```

The implementation of Redis HyperLogLog can be summarised as follows:
1. **Initialisation**: a HyperLogLog uses a fixed number of buckets to store data, and every bucket starts at zero.
2. **Adding an element**:
   - Hash the element into a bucket.
   - Update the corresponding bucket, keeping the maximum length of the leading zeros in the hash value.
3. **Estimating the cardinality**:
   - Calculate an estimate of the number of unique elements from the values in the buckets.
4. **Merging data**:
   - Merge multiple HyperLogLog data structures with the `PFMERGE` command.

#### Using Redis HyperLogLog in Go

In Go, work with it through `go-redis`: the three methods `PFAdd`, `PFCount` and `PFMerge` correspond to the three commands.

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
       err := rdb.PFAdd(ctx, "hyperloglog", "element1", "element2").Err()
       if err != nil {
           panic(err)
       }
   }
   ```

3. **Get the cardinality**
   ```go
   func example(rdb *redis.Client) {
       count, err := rdb.PFCount(ctx, "hyperloglog").Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Unique count:", count)
   }
   ```

4. **Merge HyperLogLogs**
   ```go
   func example(rdb *redis.Client) {
       err := rdb.PFMerge(ctx, "merged_hyperloglog", "hyperloglog1", "hyperloglog2").Err()
       if err != nil {
           panic(err)
       }
   }
   ```

Usage is just three methods: `PFAdd` adds elements, `PFCount` returns the estimate, and `PFMerge` merges multiple keys. Each returns an error for the caller to handle.

## References

- [Redis Official Command Manual](https://redis.io/commands/)
- [go-redis Official Client](https://github.com/redis/go-redis)
- [go-redis · pkg.go.dev](https://pkg.go.dev/github.com/redis/go-redis/v9)

## Sibling pages

- [Bitmap](/redis/Bitmap.md)
- [Geospatial](/redis/Geospatial.md)
- [Hash](/redis/Hash.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Bitmap](/redis/Bitmap.md)
- [Geospatial](/redis/Geospatial.md)
- [Hash](/redis/Hash.md)
- [Install](/redis/Install.md)
