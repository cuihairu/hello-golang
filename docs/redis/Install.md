### Redis 的安装与配置

#### 2.1 安装 Redis

1. **下载与编译**
   - 从 Redis 官方网站下载最新版本的 Redis 源码。
   - 解压源码包，并编译安装。
     ```bash
     wget http://download.redis.io/releases/redis-6.2.5.tar.gz
     tar xzf redis-6.2.5.tar.gz
     cd redis-6.2.5
     make
     ```
   - 安装完成后，可以使用 `make test` 运行测试，确保安装成功。

2. **使用包管理器安装**
   - 在不同的操作系统上，可以使用包管理器来安装 Redis。
     - **Homebrew（macOS）**：
       ```bash
       brew install redis
       ```
     - **apt（Debian/Ubuntu）**：
       ```bash
       sudo apt update
       sudo apt install redis-server
       ```
     - **yum（CentOS/RHEL）**：
       ```bash
       sudo yum install redis
       ```

3. **验证安装**
   - 装完查一下版本号：
     ```bash
     redis-server --version
     redis-cli --version
     ```

#### 2.2 配置 Redis

1. **基本配置**
   - Redis 的配置文件通常位于 `redis.conf`，可以根据需要进行修改。
   - 配置文件示例（部分）：
     ```ini
     # 端口配置
     port 6379

     # 绑定地址
     bind 127.0.0.1

     # 持久化配置
     save 900 1
     save 300 10
     save 60 10000

     # 日志级别
     loglevel notice

     # 数据库文件存储路径
     dir /var/lib/redis
     ```

2. **持久化配置**
   - Redis 支持两种持久化方式：RDB 和 AOF。
     - **RDB（快照）**：
       ```ini
       save 900 1
       save 300 10
       save 60 10000
       ```
     - **AOF（Append Only File）**：
       ```ini
       appendonly yes
       appendfilename "appendonly.aof"
       ```

3. **安全配置**
   - 设置密码保护：
     ```ini
     requirepass yourpassword
     ```
   - 限制外部访问：
     ```ini
     bind 127.0.0.1
     ```

4. **优化配置**
   - 按机器内存和使用场景调这两个参数：
     ```ini
     maxmemory 2gb
     maxmemory-policy allkeys-lru
     ```

#### 2.3 启动与停止 Redis

1. **启动 Redis**
   - 启动 Redis 服务器：
     ```bash
     redis-server /path/to/redis.conf
     ```
   - 可以使用默认配置启动：
     ```bash
     redis-server
     ```

2. **停止 Redis**
   - 使用 Redis CLI 命令停止 Redis 服务器：
     ```bash
     redis-cli shutdown
     ```
   - 如果设置了密码，需要加上 `-a` 参数：
     ```bash
     redis-cli -a yourpassword shutdown
     ```

3. **后台运行 Redis**
   - 配置 Redis 以后台模式运行：
     ```ini
     daemonize yes
     ```

到这里，Redis 已经能装、能配、能启动能停止。下一站是它的数据类型，以及在 Go 语言里怎么用。