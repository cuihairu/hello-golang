`GOPROXY` 是 Go 配置模块代理的环境变量，模块代理会缓存并转发 Go 模块的下载。在中国大陆直连官方的 `proxy.golang.org` 往往较慢，改用国内代理能明显加快下载和构建。

### 常用的国内 Go 模块代理

1. **GOPROXY.cn**
   - 地址: `https://goproxy.cn`
   - 七牛云提供的免费 Go 模块代理。

2. **goproxy.io**
   - 地址: `https://goproxy.io`
   - 主要面向全球用户的 Go 模块代理，中国大陆访问也可用。

3. **Aliyun Go 镜像**
   - 地址: `https://mirrors.aliyun.com/goproxy/`
   - 阿里云提供的 Go 模块代理，适合在中国大陆使用。

### 配置 GOPROXY

可以通过以下步骤在终端中配置 `GOPROXY` 环境变量：

```sh
export GOPROXY=https://goproxy.cn
```

或将其添加到你的 `~/.bashrc` 或 `~/.zshrc` 文件中，使其在每次打开终端时自动生效：

```sh
echo "export GOPROXY=https://goproxy.cn" >> ~/.bashrc
source ~/.bashrc
```

对于 `zsh` 用户：

```sh
echo "export GOPROXY=https://goproxy.cn" >> ~/.zshrc
source ~/.zshrc
```

### 设置多个代理

`GOPROXY` 支持配置多个代理服务器，以逗号分隔。如果第一个代理不可用，Go 工具链将自动尝试下一个。例如：

```sh
export GOPROXY=https://goproxy.cn,https://proxy.golang.org,direct
```

先试 `goproxy.cn`，失败再试 `proxy.golang.org`，最后直连源代码库。

### 验证配置

用这条命令看当前生效的配置：

```sh
go env GOPROXY
```

输出的就是当前 `GOPROXY` 的值。

### 总结

中国大陆常用的三个代理是 `goproxy.cn`、`goproxy.io` 和阿里云镜像，配好几个可以按顺序回退。

### 搭建局域网代理

在局域网内搭一个 Go 模块代理，团队成员的模块下载都走它，外网受限或太慢时也能用。下面给出两种实现：

### 使用 goproxy 的代理服务

[goproxy](https://github.com/goproxy/goproxy) 提供了一个开源的 Go 模块代理服务器，你可以在局域网内运行它。

#### 1. 安装 goproxy

先在服务器上装好 Go，然后运行：

```sh
go install github.com/goproxy/goproxy/cmd/goproxy@latest
```

#### 2. 启动 goproxy

安装完成后，可以使用以下命令启动 `goproxy`：

```sh
goproxy server --address 0.0.0.0:8080
```

这会在所有网络接口上监听 `8080` 端口，你可以根据需要更改端口号。

#### 3. 配置缓存目录（可选）

你可以配置一个缓存目录来存储下载的模块，避免重复下载。启动命令如下：

```sh
goproxy server --address 0.0.0.0:8080 --cacher dir --cacher-dir /path/to/cache
```

#### 4. 设置环境变量

在每个客户端机器上，设置 `GOPROXY` 环境变量指向你的代理服务器。例如，如果你的服务器 IP 是 `192.168.1.100`：

```sh
export GOPROXY=http://192.168.1.100:8080
```

或者将其添加到 `~/.bashrc` 或 `~/.zshrc` 文件中：

```sh
echo "export GOPROXY=http://192.168.1.100:8080" >> ~/.bashrc
source ~/.bashrc
```

### 使用 Athens 搭建 GOPROXY

[Athens](https://github.com/gomods/athens) 是另一个 Go 模块代理开源项目，用环境变量配置，存储方式可选（下例用磁盘）。

#### 1. 安装 Athens

首先，确保你的系统上已经安装了 Docker。然后，你可以使用 Docker 来运行 Athens：

```sh
docker run -d \
  --name athens \
  -p 3000:3000 \
  -v /path/to/storage:/var/lib/athens \
  gomods/athens:latest
```

这会在 `3000` 端口上运行 Athens，你可以根据需要更改端口号和存储路径。

#### 2. 配置 Athens

你可以通过环境变量来配置 Athens。例如，创建一个 `.env` 文件：

```sh
ATHENS_STORAGE_TYPE=disk
ATHENS_DISK_STORAGE_ROOT=/var/lib/athens
```

然后启动容器时加载这个文件：

```sh
docker run -d \
  --name athens \
  --env-file .env \
  -p 3000:3000 \
  -v /path/to/storage:/var/lib/athens \
  gomods/athens:latest
```

#### 3. 设置环境变量

在每个客户端机器上，设置 `GOPROXY` 环境变量指向你的 Athens 服务器。例如，如果你的服务器 IP 是 `192.168.1.100`：

```sh
export GOPROXY=http://192.168.1.100:3000
```

或者将其添加到 `~/.bashrc` 或 `~/.zshrc` 文件中：

```sh
echo "export GOPROXY=http://192.168.1.100:3000" >> ~/.bashrc
source ~/.bashrc
```

### 总结

两条路都行：想省事就用 `goproxy server` 一条命令起服务，想要更多配置项就用 Athens；客户端把 `GOPROXY` 指到那台机器即可。