### Redis 集合（Set）

Redis 集合是一种无序的字符串集合，集合中的每个元素都是唯一的，不允许重复。集合适用于需要快速查找和去重的场景，如标签系统、好友列表、推荐系统等。

#### 场景示例

1. **标签系统**
   - 示例：
     ```bash
     SADD tags "golang"
     SADD tags "redis"
     SADD tags "database"
     SMEMBERS tags
     ```
   - 说明：使用 `SADD` 添加标签，使用 `SMEMBERS` 获取所有标签。

2. **好友列表**
   - 示例：
     ```bash
     SADD friends:user1 "user2"
     SADD friends:user1 "user3"
     SADD friends:user2 "user1"
     SADD friends:user2 "user3"
     SINTER friends:user1 friends:user2
     ```
   - 说明：使用 `SADD` 添加好友，使用 `SINTER` 获取共同好友。

3. **推荐系统**
   - 示例：
     ```bash
     SADD viewed:product1 "user1"
     SADD viewed:product1 "user2"
     SADD viewed:product2 "user2"
     SADD viewed:product2 "user3"
     SUNION viewed:product1 viewed:product2
     ```
   - 说明：使用 `SADD` 记录查看产品的用户，使用 `SUNION` 获取所有查看过某些产品的用户。

4. **去重操作**
   - 示例：
     ```bash
     SADD unique:emails "user1@example.com"
     SADD unique:emails "user2@example.com"
     SADD unique:emails "user1@example.com"
     SMEMBERS unique:emails
     ```
   - 说明：使用 `SADD` 添加邮件地址，使用 `SMEMBERS` 获取唯一的邮件地址列表。

5. **随机获取元素**
   - 示例：
     ```bash
     SADD colors "red" "green" "blue"
     SRANDMEMBER colors
     ```
   - 说明：使用 `SADD` 添加颜色，使用 `SRANDMEMBER` 随机获取一个颜色。

#### 底层实现

Redis 集合的底层实现主要基于两种数据结构：`intset`（整数集合）和 `hashtable`（哈希表）。

1. **整数集合（intset）**
   - 当集合中的所有元素都是整数且数量较少时，Redis 使用整数集合存储集合。整数集合是一种紧凑的编码方式，节省内存。
   - 结构：
     ```c
     typedef struct intset {
         uint32_t encoding;        // 编码方式
         uint32_t length;          // 集合中元素的数量
         int8_t contents[];        // 元素数组
     } intset;
     ```
   - 优点：内存占用小，适合存储小规模整数集合。

2. **哈希表（hashtable）**
   - 当集合中的元素类型复杂或数量较多时，Redis 使用哈希表存储集合。哈希表提供快速的查找、插入和删除操作。
   - 结构：
     ```c
     typedef struct dictht {
         dictEntry **table;        // 哈希表数组
         unsigned long size;       // 哈希表大小
         unsigned long sizemask;   // 哈希表大小掩码，用于计算索引
         unsigned long used;       // 已使用节点数量
     } dictht;
     
     typedef struct dictEntry {
         void *key;                // 键
         void *val;                // 值（在集合中为 NULL）
         struct dictEntry *next;   // 链表指针，解决冲突
     } dictEntry;
     ```
   - 优点：高效处理大规模数据，查找速度快。

Redis 会根据集合的元素类型和数量，动态选择最合适的数据结构进行存储，从而在性能和内存使用之间取得平衡。

#### Go 中使用 Redis 集合

在 Go 语言中，可以使用 `go-redis` 库来操作 Redis 集合。下面是一些基本操作示例。

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

3. **获取所有元素**
   ```go
   func example(rdb *redis.Client) {
       members, err := rdb.SMembers(ctx, "tags").Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Tags:", members)
   }
   ```

4. **检查元素是否存在**
   ```go
   func example(rdb *redis.Client) {
       exists, err := rdb.SIsMember(ctx, "tags", "golang").Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Is 'golang' a member of tags?", exists)
   }
   ```

5. **删除元素**
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

6. **随机获取元素**
   ```go
   func example(rdb *redis.Client) {
       member, err := rdb.SRandMember(ctx, "tags").Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Random tag:", member)
   }
   ```

通过这些示例，可以在 Go 语言中方便地操作 Redis 集合，实现各种常见场景的需求。