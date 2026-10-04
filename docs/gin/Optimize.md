# 路由性能优化

#### 9.1 路由树结构解析

Gin 的路由存在前缀树里，匹配请求路径就是沿树走一遍。要优化路由，先得看懂这棵树。

##### 9.1.1 路由树概述

Gin 的路由树是一种前缀树（Trie），每个节点代表 URL 路径的一段，匹配时逐段比较。

##### 9.1.2 路由节点

路由树的每个节点包含以下信息：
- `path`：当前节点对应的路径部分。
- `indices`：子节点的索引，用于快速查找。
- `children`：子节点列表。
- `handlers`：对应当前路径的处理函数。

##### 9.1.3 路由树的构建

路由树在注册路由时动态构建，通过将路径按部分分解，并逐级插入节点来构建树结构。

```go
func (r *router) addRoute(method, path string, handlers HandlersChain) {
    root := r.trees[method]
    if root == nil {
        root = new(node)
        r.trees[method] = root
    }
    root.addRoute(path, handlers)
}
```

#### 9.2 路由匹配优化

##### 9.2.1 路径规范化

在进行路由匹配前，规范化路径（如去除多余的斜杠、统一大小写）可以减少匹配的复杂度。

```go
func normalizePath(path string) string {
    // 实现路径规范化逻辑
    return path
}
```

##### 9.2.2 提前匹配静态部分

对于包含静态部分和动态参数的路径，优先匹配静态部分可以快速排除不匹配的路径，从而提高匹配效率。

```go
func (n *node) getValue(path string, params *Params, unescape bool) (value HandlersChain, tsr bool) {
    for len(path) >= len(n.path) {
        if path[:len(n.path)] == n.path {
            // 处理静态部分匹配
        }
    }
    // 处理动态部分匹配
    return nil, false
}
```

##### 9.2.3 路径缓存

对经常访问的路径进行缓存，可以避免重复计算，直接从缓存中获取匹配结果。

```go
var pathCache = make(map[string]HandlersChain)

func (r *router) getCachedRoute(method, path string) HandlersChain {
    if handlers, ok := pathCache[path]; ok {
        return handlers
    }
    return nil
}

func (r *router) handleRequest(c *Context) {
    handlers := r.getCachedRoute(c.Request.Method, c.Request.URL.Path)
    if handlers != nil {
        c.handlers = handlers
        c.Next()
        return
    }
    // 正常路由匹配逻辑
}
```

#### 9.3 高效的路由查找算法

查找算法决定匹配时要比较多少次，有三种常见思路。

##### 9.3.1 前缀树算法

Gin 使用前缀树（Trie）算法，通过逐级匹配路径部分，减少匹配的复杂度。

```go
func (n *node) addRoute(path string, handlers HandlersChain) {
    for len(path) > 0 {
        // 插入节点逻辑
    }
}
```

##### 9.3.2 二分查找

对于具有多个子节点的情况，可以使用二分查找来提高查找效率。

```go
func (n *node) getValue(path string, params *Params, unescape bool) (value HandlersChain, tsr bool) {
    low, high := 0, len(n.children)-1
    for low <= high {
        mid := (low + high) / 2
        if path[mid] < n.children[mid].path[0] {
            high = mid - 1
        } else if path[mid] > n.children[mid].path[0] {
            low = mid + 1
        } else {
            // 处理匹配
            break
        }
    }
    // 继续匹配剩余路径
    return nil, false
}
```

##### 9.3.3 哈希表

对于大量静态路由，可以使用哈希表来加速匹配。

```go
type router struct {
    trees map[string]*node
    staticRoutes map[string]HandlersChain
}

func (r *router) addStaticRoute(method, path string, handlers HandlersChain) {
    if r.staticRoutes == nil {
        r.staticRoutes = make(map[string]HandlersChain)
    }
    r.staticRoutes[path] = handlers
}

func (r *router) getStaticRoute(method, path string) HandlersChain {
    if handlers, ok := r.staticRoutes[path]; ok {
        return handlers
    }
    return nil
}
```

### 总结

Gin 的路由匹配走前缀树：先做路径规范化，静态段优先比较，命中缓存就跳过整棵树。子节点多时用二分查找，静态路由多时用哈希表，都是把比较次数降下来的手段。