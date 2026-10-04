### Redis 字符串（String）

Redis 的字符串类型是最基本的数据类型，文本、数字、二进制数据都能存。先看八个常见场景，再看底层的 `SDS`。

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

Redis 字符串的底层是 `SDS`（Simple Dynamic String，简单动态字符串）。它在 C 语言 `char` 数组外面包了一层，长度和剩余空间记在头部。`SDS` 的实现特点：

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

`SDS` 自己记长度，C 字符串常见的缓冲区溢出和反复分配就绕开了；预分配也让追加、计数这类操作少做几次内存分配。前面八个场景——存储、计数、拼接、位操作、数值操作——都建立在这一层之上。