### Redis 地理空间数据（Geospatial）

Redis 能存储、查询地理位置数据，底层基于 **Geohash** 编码，对外是一组 `GEO` 开头的命令。

#### 场景示例

1. **附近地点搜索**
   - 示例：寻找某个地点周围的商店或餐馆。
     ```bash
     GEOADD locations 13.361389 38.115556 "Palermo"
     GEOADD locations 15.087269 37.502669 "Catania"
     GEORADIUS locations 15 37 200 km
     ```
   - 说明：`GEOADD` 添加地理位置，`GEORADIUS` 查找半径内的地点。

2. **用户位置追踪**
   - 示例：追踪移动用户的位置并查询附近的其他用户。
     ```bash
     GEOADD user_locations 13.361389 38.115556 "user1"
     GEOADD user_locations 15.087269 37.502669 "user2"
     GEORADIUS user_locations 13.5 38.1 10 km
     ```
   - 说明：`GEOADD` 添加用户位置，`GEORADIUS` 查找附近的用户。

3. **物流配送优化**
   - 示例：在配送中心周围查找客户以优化配送路线。
     ```bash
     GEOADD delivery_points 12.496366 41.902782 "Rome"
     GEOADD delivery_points 13.361389 38.115556 "Palermo"
     GEORADIUS delivery_points 12.5 41.9 50 km
     ```
   - 说明：`GEOADD` 添加配送点，`GEORADIUS` 查找配送点半径内的客户。

4. **运动活动分析**
   - 示例：记录运动员的跑步轨迹并分析跑步路线。
     ```bash
     GEOADD athlete_path 13.361389 38.115556 "start_point"
     GEOADD athlete_path 15.087269 37.502669 "end_point"
     ```
   - 说明：`GEOADD` 记录轨迹点，`GEORADIUS` 查询特定区域内的活动点。

#### 底层实现

Geohash 是把地理位置（经度和纬度）编码成短字符串的算法，Redis 靠它存储和查询位置数据。

1. **数据结构**
   - Redis 内部使用 **Sorted Set**（有序集合）来存储地理位置数据。每个位置在 Sorted Set 中都有一个唯一的成员，成员的分数由其地理位置的经度和纬度决定。
   - **Geohash** 编码将经纬度数据映射到一个唯一的字符串，这个字符串用于进行空间查询和计算。

2. **主要命令**
   - **GEOADD**：添加地理位置到 Redis 数据库。
     ```bash
     GEOADD key longitude latitude member [longitude latitude member ...]
     ```
   - **GEOPOS**：获取存储在 Redis 中的地理位置的经纬度。
     ```bash
     GEOPOS key member [member ...]
     ```
   - **GEODIST**：计算两个地理位置之间的距离。
     ```bash
     GEODIST key member1 member2 [unit]
     ```
   - **GEORADIUS**：查找指定半径内的所有地理位置。
     ```bash
     GEORADIUS key longitude latitude radius [unit] [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count]
     ```
   - **GEORADIUSBYMEMBER**：基于存储在 Redis 中的成员查找半径内的地理位置。
     ```bash
     GEORADIUSBYMEMBER key member radius [unit] [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count]
     ```

3. **编码与解码**
   - **Geohash 编码**：Redis 使用 Geohash 将经纬度编码为一个唯一的字符串。Geohash 是一种紧凑的字符串表示法，用于地理数据的空间索引。
   - **解码**：从 Geohash 字符串中恢复经纬度数据，以便进行进一步的计算和查询。

#### Go 中使用 Redis 地理空间功能

在 Go 语言中，可以使用 `go-redis` 库来操作 Redis 的地理空间数据。以下是一些基本操作示例。

1. **连接 Redis**
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

       // 示例代码调用
       example(rdb)
   }

   func example(rdb *redis.Client) {
       // 示例操作
   }
   ```

2. **添加地理位置**
   ```go
   func example(rdb *redis.Client) {
       _, err := rdb.GeoAdd(ctx, "locations", &redis.GeoLocation{
           Name:      "Palermo",
           Longitude: 13.361389,
           Latitude:  38.115556,
       }).Result()
       if err != nil {
           panic(err)
       }
   }
   ```

3. **查询地理位置**
   ```go
   func example(rdb *redis.Client) {
       pos, err := rdb.GeoPos(ctx, "locations", "Palermo").Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Palermo coordinates:", pos)
   }
   ```

4. **计算距离**
   ```go
   func example(rdb *redis.Client) {
       dist, err := rdb.GeoDist(ctx, "locations", "Palermo", "Catania", "km").Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Distance between Palermo and Catania:", dist)
   }
   ```

5. **查找半径内的地点**
   ```go
   func example(rdb *redis.Client) {
       locations, err := rdb.GeoRadius(ctx, "locations", 15, 37, &redis.GeoRadiusQuery{
           Radius: 200, // 半径
           Unit:   "km", // 单位：m、km、ft、mi
       }).Result()
       if err != nil {
           panic(err)
       }
       for _, loc := range locations {
           fmt.Println("Location:", loc.Name)
       }
   }
   ```

常用组合就三条：`GEOADD` 存点，`GEORADIUS` 和 `GEORADIUSBYMEMBER` 按半径圈点，`GEODIST` 算两点距离。