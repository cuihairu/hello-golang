# Optimizing route performance

#### 9.1 Understanding the route tree structure

Gin keeps its routes in a prefix tree; matching a request path is just one walk down the tree. To optimize routing, you first have to understand that tree.

##### 9.1.1 Route tree overview

Gin's route tree is a prefix tree (Trie). Each node stands for one segment of a URL path, and matching compares segment by segment.

##### 9.1.2 Route nodes

Each node of the route tree holds the following:
- `path`: the path segment this node corresponds to.
- `indices`: an index over the child nodes, used for fast lookup.
- `children`: the list of child nodes.
- `handlers`: the handler functions for this path.

##### 9.1.3 Building the route tree

The route tree is built dynamically as routes are registered: the path is split into segments and nodes are inserted level by level to form the tree.

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

#### 9.2 Optimizing route matching

##### 9.2.1 Path normalization

Normalizing the path before matching (removing redundant slashes, unifying case, and so on) reduces the complexity of the match.

```go
func normalizePath(path string) string {
    // implement the path normalization logic
    return path
}
```

##### 9.2.2 Matching static parts first

For paths that mix static segments with dynamic parameters, matching the static part first quickly rules out paths that can't match, which speeds things up.

```go
func (n *node) getValue(path string, params *Params, unescape bool) (value HandlersChain, tsr bool) {
    for len(path) >= len(n.path) {
        if path[:len(n.path)] == n.path {
            // handle the static segment match
        }
    }
    // handle the dynamic segment match
    return nil, false
}
```

##### 9.2.3 Path caching

Caching frequently visited paths avoids repeating the work: the match result is read straight from the cache.

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
    // the usual route matching logic
}
```

#### 9.3 Efficient route lookup algorithms

The lookup algorithm decides how many comparisons matching takes. There are three common approaches.

##### 9.3.1 Prefix tree algorithm

Gin uses a prefix tree (Trie), matching path segments step by step to reduce the complexity of the match.

```go
func (n *node) addRoute(path string, handlers HandlersChain) {
    for len(path) > 0 {
        // logic that inserts the node
    }
}
```

##### 9.3.2 Binary search

When a node has many children, binary search can make the lookup faster.

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
            // handle the match
            break
        }
    }
    // keep matching the rest of the path
    return nil, false
}
```

##### 9.3.3 Hash tables

For a large number of static routes, a hash table can speed up matching.

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

### Summary

Gin matches routes on a prefix tree: normalize the path, compare static segments first, and skip the whole tree if the cache has a hit. Binary search when a node has many children, a hash table when there are many static routes — both just cut the number of comparisons.

## References

- [Gin Official Documentation](https://gin-gonic.com/en/docs/)
- [Gin · pkg.go.dev](https://pkg.go.dev/github.com/gin-gonic/gin)


## Sibling pages

- [Config](/gin/Config.md)
- [Debug](/gin/Debug.md)
- [Error](/gin/Error.md)
- [Middleware](/gin/Middleware.md)
- [Request](/gin/Request.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Middleware](/gin/Middleware.md)
- [Request](/gin/Request.md)
