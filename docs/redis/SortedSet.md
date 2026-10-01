### Redis 有序集合（Sorted Set）

Redis 有序集合（Sorted Set）是一种带有分数的字符串集合，每个成员都有一个唯一的分数，Redis 会根据分数进行排序。它适用于排行榜、延时队列等场景。

#### 场景示例

1. **排行榜**
   - 示例：
     ```bash
     ZADD leaderboard 100 "user1"
     ZADD leaderboard 200 "user2"
     ZADD leaderboard 150 "user3"
     ZRANGE leaderboard 0 -1 WITHSCORES
     ```
   - 说明：使用 `ZADD` 添加用户及其分数，使用 `ZRANGE` 获取排行榜。

2. **延时队列**
   - 示例：
     ```bash
     ZADD delay_queue 1627474800 "task1"
     ZADD delay_queue 1627478400 "task2"
     ZRANGEBYSCORE delay_queue -inf 1627478400
     ```
   - 说明：使用 `ZADD` 添加任务及其执行时间，使用 `ZRANGEBYSCORE` 获取到期任务。

3. **事件调度**
   - 示例：
     ```bash
     ZADD schedule 1627474800 "event1"
     ZADD schedule 1627478400 "event2"
     ZRANGEBYSCORE schedule -inf +inf
     ```
   - 说明：使用 `ZADD` 添加事件及其时间，使用 `ZRANGEBYSCORE` 获取所有事件。

4. **排名查询**
   - 示例：
     ```bash
     ZADD scores 90 "Alice"
     ZADD scores 80 "Bob"
     ZADD scores 95 "Charlie"
     ZRANK scores "Alice"
     ```
   - 说明：使用 `ZADD` 添加用户及其分数，使用 `ZRANK` 获取用户排名。

5. **范围查询**
   - 示例：
     ```bash
     ZADD temperatures 20 "New York"
     ZADD temperatures 25 "Los Angeles"
     ZADD temperatures 15 "Chicago"
     ZRANGEBYSCORE temperatures 15 25
     ```
   - 说明：使用 `ZADD` 添加城市及其温度，使用 `ZRANGEBYSCORE` 获取指定范围内的城市。

#### 底层实现

Redis 有序集合的底层实现主要基于两种数据结构：`ziplist`（压缩列表）和 `skiplist`（跳跃表）。

1. **压缩列表（ziplist）**
   - 当有序集合中的元素较少且每个元素的长度较短时，Redis 使用压缩列表存储有序集合。压缩列表是一种紧凑的内存结构，可以高效存储小规模数据。
   - 结构：
     ```c
     typedef struct ziplist {
         unsigned char *zlbytes;   // 压缩列表的字节数组
         unsigned char *zltail;    // 压缩列表尾部指针
         unsigned int zllen;       // 压缩列表长度
         unsigned char *entries;   // 列表项
     } ziplist;
     ```
   - 优点：内存占用小，适合存储小规模有序集合。

2. **跳跃表（skiplist）**
   - 当有序集合中的元素较多或每个元素的长度较长时，Redis 使用跳跃表存储有序集合。跳跃表是一种高效的有序数据结构，支持快速插入、删除和查找操作。
   - 结构：
     ```c
     typedef struct zskiplistNode {
         sds ele;                           // 元素
         double score;                      // 分数
         struct zskiplistNode *backward;    // 后退指针
         struct zskiplistLevel {
             struct zskiplistNode *forward; // 前进指针
             unsigned int span;             // 跨度
         } level[];
     } zskiplistNode;

     typedef struct zskiplist {
         struct zskiplistNode *header;      // 表头节点
         struct zskiplistNode *tail;        // 表尾节点
         unsigned long length;              // 长度
         int level;                         // 层数
     } zskiplist;
     ```
   - 优点：高效处理大规模数据，查找速度快。

Redis 会根据有序集合的元素数量和每个元素的长度，动态选择最合适的数据结构进行存储，从而在性能和内存使用之间取得平衡。

#### Go 中使用 Redis 有序集合

在 Go 语言中，可以使用 `go-redis` 库来操作 Redis 有序集合。下面是一些基本操作示例。

1. **连接 Redis**
   ```go
   package main

   import (
       "github.com/go-redis/redis/v8"
       "context"
       "fmt"
   )

   var ctx = context.Background()

   func main() {
       rdb := redis.NewClient(&redis.Options{
           Addr:     "localhost:6379",
           Password: "", // no password set
           DB:       0,  // use default DB
       })

       // 示例代码调用
       example(rdb)
   }

   func example(rdb *redis.Client) {
       // 示例操作
   }
   ```

2. **添加元素**
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

3. **获取所有元素**
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

4. **检查元素是否存在**
   ```go
   func example(rdb *redis.Client) {
       score, err := rdb.ZScore(ctx, "leaderboard", "user1").Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Score of 'user1':", score)
   }
   ```

5. **删除元素**
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

6. **范围查询**
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

通过这些示例，可以在 Go 语言中方便地操作 Redis 有序集合，实现各种常见场景的需求。