### Redis 字符串（String）

Redis 的字符串类型是最基本的数据类型，可以存储任何形式的字符串，包括文本、数字、二进制数据等。下面是一些使用字符串的常见场景及其底层实现。

#### 场景示例

1. **存储简单的键值对**
   - 示例：
     ```bash
     SET key "value"
     GET key
     ```
   - 说明：将键 `key` 的值设置为 `value`，然后获取该值。

2. **计数器**
   - 示例：
     ```bash
     INCR page_view_count
     GET page_view_count
     ```
   - 说明：将键 `page_view_count` 的值增加 1，用于记录页面浏览次数。

3. **存储二进制数据**
   - 示例：
     ```bash
     SET image_data "\x89PNG..."
     GET image_data
     ```
   - 说明：可以存储二进制数据，如图像或文件。

4. **过期时间的键值**
   - 示例：
     ```bash
     SET session_token "abc123" EX 3600
     GET session_token
     ```
   - 说明：设置键 `session_token` 的值并设置过期时间为 3600 秒。

5. **批量操作**
   - 示例：
     ```bash
     MSET key1 "value1" key2 "value2"
     MGET key1 key2
     ```
   - 说明：一次性设置多个键值对，并获取多个键的值。

6. **字符串操作**
   - 示例：
     ```bash
     APPEND key "suffix"
     GETRANGE key 0 4
     ```
   - 说明：将字符串 `suffix` 附加到 `key` 的值末尾，并获取 `key` 的部分值。

7. **位操作**
   - 示例：
     ```bash
     SETBIT bitkey 7 1
     GETBIT bitkey 7
     BITCOUNT bitkey
     ```
   - 说明：使用位操作设置、获取和统计位。

8. **数值操作**
   - 示例：
     ```bash
     INCRBYFLOAT price 12.34
     DECR quantity
     ```
   - 说明：对数值进行增减操作。

#### 底层实现

Redis 字符串类型的底层实现主要依赖于 `SDS`（Simple Dynamic String，简单动态字符串）。`SDS` 是 Redis 对 C 语言 `char` 数组的封装，提供了更安全、更高效的字符串操作。以下是 `SDS` 的实现特点：

1. **动态扩展**：
   - `SDS` 支持动态扩展，字符串增长时会自动分配足够的空间，减少内存分配次数。
   - 示例代码：
     ```c
     struct sdshdr {
         int len;       // 已使用长度
         int free;      // 可用空间
         char buf[];    // 数据缓冲区
     };
     ```

2. **二进制安全**：
   - `SDS` 可以存储任意二进制数据，包括空字符，因为它通过 `len` 属性记录字符串长度，而不是以空字符结尾。

3. **预分配**：
   - `SDS` 在扩展时会预分配空间，减少后续扩展的内存分配开销。
   - 扩展规则：如果新长度小于 1MB，则分配两倍的新长度；否则分配 1MB 的增量空间。

4. **兼容 C 字符串**：
   - `SDS` 可以与 C 字符串兼容，`buf` 末尾始终保留一个空字符，但不计入 `len`。

5. **内存效率**：
   - `SDS` 通过合理的内存管理和扩展策略，减少了内存碎片，提高了内存利用效率。

`SDS` 使得 Redis 在处理字符串时既能保持高性能，又能避免 C 语言 `char` 数组的常见问题，如缓冲区溢出和频繁的内存分配。通过这些特性，Redis 能够高效地处理各种字符串操作，包括存储、获取、计数、字符串拼接、位操作和数值操作。