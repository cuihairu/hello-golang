### Redis 哈希（Hash）

Redis 哈希是一个键值对集合，适用于存储对象。每个哈希是一个键与多个字段及其值的映射。哈希非常适合用于表示具有多个属性的对象，如用户信息。

#### 场景示例

1. **存储和获取用户信息**
   - 示例：
     ```bash
     HSET user:1000 name "Alice" age "30" email "alice@example.com"
     HGETALL user:1000
     ```
   - 说明：使用 `HSET` 命令存储用户信息，并使用 `HGETALL` 获取所有字段和值。

2. **更新特定字段**
   - 示例：
     ```bash
     HSET user:1000 age "31"
     HGET user:1000 age
     ```
   - 说明：使用 `HSET` 更新用户的年龄，并使用 `HGET` 获取特定字段的值。

3. **删除字段**
   - 示例：
     ```bash
     HDEL user:1000 email
     HGETALL user:1000
     ```
   - 说明：使用 `HDEL` 删除用户的 email 字段，并使用 `HGETALL` 获取所有字段和值。

4. **字段存在性检查**
   - 示例：
     ```bash
     HEXISTS user:1000 email
     ```
   - 说明：使用 `HEXISTS` 检查某字段是否存在。

5. **获取所有字段**
   - 示例：
     ```bash
     HKEYS user:1000
     ```
   - 说明：使用 `HKEYS` 获取所有字段名称。

6. **获取所有值**
   - 示例：
     ```bash
     HVALS user:1000
     ```
   - 说明：使用 `HVALS` 获取所有字段的值。

7. **增加字段值**
   - 示例：
     ```bash
     HINCRBY user:1000 age 1
     HGET user:1000 age
     ```
   - 说明：使用 `HINCRBY` 增加字段的数值，并使用 `HGET` 获取字段的值。

#### 底层实现

Redis 哈希底层实现主要基于两种数据结构：`ziplist`（压缩列表）和 `hashtable`（哈希表）。

1. **压缩列表（ziplist）**
   - 当哈希包含的键值对数量较少且每个键值对的长度较短时，Redis 使用压缩列表存储哈希。压缩列表是一种经过特殊编码的连续内存块，节省空间。
   - 结构：
     ```c
     struct {
         unsigned int zlbytes;     // 压缩列表的总字节数
         unsigned int zltail;      // 到达表尾的偏移量
         unsigned int zllen;       // 压缩列表包含的节点数量
         unsigned char entries[];  // 数据节点
     };
     ```
   - 优点：紧凑内存布局，适合存储小数据量。

2. **哈希表（hashtable）**
   - 当哈希包含的键值对数量较多或某些键值对的长度较长时，Redis 使用哈希表存储哈希。哈希表提供快速的查找、插入和删除操作。
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
         void *val;                // 值
         struct dictEntry *next;   // 链表指针，解决冲突
     } dictEntry;
     ```
   - 优点：高效处理大数据量和长字符串。

Redis 通过内存占用和访问速度的权衡，选择最合适的数据结构来存储哈希数据。开始时，Redis 使用压缩列表存储小型哈希，当哈希增长到一定规模时，自动转换为哈希表，从而兼顾空间效率和性能。