### Redis Geospatial

Redis can store and query geographic location data. Under the hood it is based on **Geohash** encoding, exposed as a set of commands that start with `GEO`.

#### Scenario examples

1. **Nearby location search**
   - Example: find shops or restaurants around a given location.
     ```bash
     GEOADD locations 13.361389 38.115556 "Palermo"
     GEOADD locations 15.087269 37.502669 "Catania"
     GEORADIUS locations 15 37 200 km
     ```
   - Note: `GEOADD` adds a geographic location, and `GEORADIUS` finds the locations within a radius.

2. **User location tracking**
   - Example: track the location of a mobile user and query nearby users.
     ```bash
     GEOADD user_locations 13.361389 38.115556 "user1"
     GEOADD user_locations 15.087269 37.502669 "user2"
     GEORADIUS user_locations 13.5 38.1 10 km
     ```
   - Note: `GEOADD` adds a user's location, and `GEORADIUS` finds nearby users.

3. **Logistics route optimization**
   - Example: find customers around a distribution centre to optimise delivery routes.
     ```bash
     GEOADD delivery_points 12.496366 41.902782 "Rome"
     GEOADD delivery_points 13.361389 38.115556 "Palermo"
     GEORADIUS delivery_points 12.5 41.9 50 km
     ```
   - Note: `GEOADD` adds delivery points, and `GEORADIUS` finds the customers within the delivery radius.

4. **Sports activity analysis**
   - Example: record an athlete's running route and analyse the path.
     ```bash
     GEOADD athlete_path 13.361389 38.115556 "start_point"
     GEOADD athlete_path 15.087269 37.502669 "end_point"
     ```
   - Note: `GEOADD` records a point on the route, and `GEORADIUS` queries the activity points within a given area.

#### Underlying implementation

Geohash is an algorithm that encodes a geographic location (longitude and latitude) into a short string. Redis relies on it to store and query location data.

1. **Data structure**
   - Internally Redis uses a **Sorted Set** to store geographic location data. Each location has a unique member in the Sorted Set, and the member's score is determined by its longitude and latitude.
   - **Geohash** encoding maps longitude and latitude data into a unique string, which is used for spatial queries and calculations.

2. **Main commands**
   - **GEOADD**: add a geographic location to the Redis database.
     ```bash
     GEOADD key longitude latitude member [longitude latitude member ...]
     ```
   - **GEOPOS**: get the longitude and latitude of a geographic location stored in Redis.
     ```bash
     GEOPOS key member [member ...]
     ```
   - **GEODIST**: calculate the distance between two geographic locations.
     ```bash
     GEODIST key member1 member2 [unit]
     ```
   - **GEORADIUS**: find all geographic locations within a given radius.
     ```bash
     GEORADIUS key longitude latitude radius [unit] [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count]
     ```
   - **GEORADIUSBYMEMBER**: find locations within a radius based on a member stored in Redis.
     ```bash
     GEORADIUSBYMEMBER key member radius [unit] [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count]
     ```

3. **Encoding and decoding**
   - **Geohash encoding**: Redis uses Geohash to encode longitude and latitude into a unique string. Geohash is a compact string representation used for spatial indexing of geographic data.
   - **Decoding**: recover longitude and latitude data from a Geohash string, so that further calculations and queries can be done.

#### Using Redis Geospatial Features in Go

In Go, you can use the `go-redis` library to work with Redis geospatial data. Here are some basic operations.

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

2. **Add a geographic location**
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

3. **Query a geographic location**
   ```go
   func example(rdb *redis.Client) {
       pos, err := rdb.GeoPos(ctx, "locations", "Palermo").Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Palermo coordinates:", pos)
   }
   ```

4. **Calculate the distance**
   ```go
   func example(rdb *redis.Client) {
       dist, err := rdb.GeoDist(ctx, "locations", "Palermo", "Catania", "km").Result()
       if err != nil {
           panic(err)
       }
       fmt.Println("Distance between Palermo and Catania:", dist)
   }
   ```

5. **Find locations within a radius**
   ```go
   func example(rdb *redis.Client) {
       locations, err := rdb.GeoRadius(ctx, "locations", 15, 37, &redis.GeoRadiusQuery{
           Radius: 200, // radius
           Unit:   "km", // unit: m, km, ft, mi
       }).Result()
       if err != nil {
           panic(err)
       }
       for _, loc := range locations {
           fmt.Println("Location:", loc.Name)
       }
   }
   ```

The common combinations come down to three: `GEOADD` to store points, `GEORADIUS` and `GEORADIUSBYMEMBER` to pick out points by radius, and `GEODIST` to compute the distance between two points.

## References

- [Redis Official Command Manual](https://redis.io/commands/)
- [go-redis Official Client](https://github.com/redis/go-redis)
- [go-redis · pkg.go.dev](https://pkg.go.dev/github.com/redis/go-redis/v9)

## Sibling pages

- [Bitmap](/redis/Bitmap.md)
- [Hash](/redis/Hash.md)
- [HyperLogLog](/redis/HyperLogLog.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Bitmap](/redis/Bitmap.md)
- [Hash](/redis/Hash.md)
- [HyperLogLog](/redis/HyperLogLog.md)
- [Install](/redis/Install.md)
- [List](/redis/List.md)
- [Readme](/redis/Readme.md)
- [Set](/redis/Set.md)
- [SortedSet](/redis/SortedSet.md)
- [Streams](/redis/Streams.md)
- [String](/redis/String.md)
