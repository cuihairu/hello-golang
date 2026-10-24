### Installing and Configuring Redis

#### 2.1 Installing Redis

1. **Download and compile**
   - Download the latest version of the Redis source code from the official Redis website.
   - Unpack the source tarball, then compile and install.
     ```bash
     wget http://download.redis.io/releases/redis-6.2.5.tar.gz
     tar xzf redis-6.2.5.tar.gz
     cd redis-6.2.5
     make
     ```
   - After installing, you can run the tests with `make test` to make sure the install succeeded.

2. **Install with a package manager**
   - On different operating systems, you can use a package manager to install Redis.
     - **Homebrew (macOS)**:
       ```bash
       brew install redis
       ```
     - **apt (Debian/Ubuntu)**:
       ```bash
       sudo apt update
       sudo apt install redis-server
       ```
     - **yum (CentOS/RHEL)**:
       ```bash
       sudo yum install redis
       ```

3. **Verify the install**
   - Once it's installed, check the version:
     ```bash
     redis-server --version
     redis-cli --version
     ```

#### 2.2 Configuring Redis

1. **Basic configuration**
   - The Redis config file is usually at `redis.conf`; modify it as needed.
   - Config file example (partial):
     ```ini
     # port configuration
     port 6379

     # bind address
     bind 127.0.0.1

     # persistence configuration
     save 900 1
     save 300 10
     save 60 10000

     # log level
     loglevel notice

     # database file storage path
     dir /var/lib/redis
     ```

2. **Persistence configuration**
   - Redis supports two persistence methods: RDB and AOF.
     - **RDB (snapshots)**:
       ```ini
       save 900 1
       save 300 10
       save 60 10000
       ```
     - **AOF (Append Only File)**:
       ```ini
       appendonly yes
       appendfilename "appendonly.aof"
       ```

3. **Security configuration**
   - Set a password:
     ```ini
     requirepass yourpassword
     ```
   - Restrict external access:
     ```ini
     bind 127.0.0.1
     ```

4. **Tuning configuration**
   - Tune these two parameters for your machine's memory and your use case:
     ```ini
     maxmemory 2gb
     maxmemory-policy allkeys-lru
     ```

#### 2.3 Starting and Stopping Redis

1. **Start Redis**
   - Start the Redis server:
     ```bash
     redis-server /path/to/redis.conf
     ```
   - You can also start it with the default configuration:
     ```bash
     redis-server
     ```

2. **Stop Redis**
   - Use the Redis CLI command to stop the Redis server:
     ```bash
     redis-cli shutdown
     ```
   - If you set a password, you need to add the `-a` flag:
     ```bash
     redis-cli -a yourpassword shutdown
     ```

3. **Run Redis in the background**
   - Configure Redis to run in daemon mode:
     ```ini
     daemonize yes
     ```

At this point, Redis can be installed, configured, started, and stopped. Next stop is its data types, and how to use them in Go.

## References

- [Redis Official Command Manual](https://redis.io/commands/)
- [go-redis Official Client](https://github.com/redis/go-redis)
- [go-redis · pkg.go.dev](https://pkg.go.dev/github.com/redis/go-redis/v9)


## Sibling pages

- [Bitmap](/redis/Bitmap.md)
- [Geospatial](/redis/Geospatial.md)
- [Hash](/redis/Hash.md)
- [HyperLogLog](/redis/HyperLogLog.md)
- [List](/redis/List.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [List](/redis/List.md)
