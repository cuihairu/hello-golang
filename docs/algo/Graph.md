### 图

图（Graph）由顶点和边组成，描述"多对多"的关系：社交网络的好友关系、依赖任务的先后顺序、网络路由，都是图的形态。同目录的 [最小生成树](MinimumSpanningTree.md) 讲加权图上的经典算法，这一页讲图的表示和两种遍历。

### 邻接表表示

Go 里最常用的表示法是 `map` + 切片：每个顶点映射到它的邻居列表。无向图的边要登记两次：

```go
type Graph struct {
	adj map[int][]int
}

func NewGraph() *Graph { return &Graph{adj: make(map[int][]int)} }

func (g *Graph) AddEdge(u, v int) {
	g.adj[u] = append(g.adj[u], v)
	g.adj[v] = append(g.adj[v], u)
}
```

顶点编号密集时用 `[][]int` 切片代替 map，访问更快；带权图把邻居换成结构体（顶点 + 权重）。

### 遍历：BFS 与 DFS

广度优先（BFS）按层扩散，用队列；深度优先（DFS）一条路走到黑，用栈（或递归）。两者都靠 `visited` 集合防止绕圈：

```go
func (g *Graph) BFS(start int) []int {
	visited := make(map[int]bool)
	queue := []int{start}
	visited[start] = true
	order := []int{}
	for len(queue) > 0 {
		u := queue[0]
		queue = queue[1:]
		order = append(order, u)
		for _, v := range g.adj[u] {
			if !visited[v] {
				visited[v] = true
				queue = append(queue, v)
			}
		}
	}
	return order
}

func (g *Graph) DFS(start int) []int {
	visited := make(map[int]bool)
	stack := []int{start}
	order := []int{}
	for len(stack) > 0 {
		u := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if visited[u] {
			continue
		}
		visited[u] = true
		order = append(order, u)
		for i := len(g.adj[u]) - 1; i >= 0; i-- {
			v := g.adj[u][i]
			if !visited[v] {
				stack = append(stack, v)
			}
		}
	}
	return order
}

func main() {
	g := NewGraph()
	g.AddEdge(0, 1)
	g.AddEdge(0, 2)
	g.AddEdge(1, 3)
	g.AddEdge(2, 3)
	g.AddEdge(3, 4)

	fmt.Println("BFS from 0:", g.BFS(0)) // 输出：BFS from 0: [0 1 2 3 4]
	fmt.Println("DFS from 0:", g.DFS(0)) // 输出：DFS from 0: [0 1 3 2 4]
}
```

两个遍历都是 O(V+E)：每个顶点进出容器一次，每条边看两次。

### 怎么选

- **无权图最短路径、层序问题** → BFS，第一次到达某顶点的路径就是最短路径。
- **连通性、环路检测、需要回溯的问题**（拓扑排序、迷宫）→ DFS。
- DFS 的递归写法更短，但深度可能超过栈的限制；显式栈的版本没有这个顾虑。

### 小结

邻接表配 map 是 Go 里表示图的基本盘；BFS 队列、DFS 栈，visited 集合是防环的关键。加权图上的最短路径与最小生成树见 [最小生成树](MinimumSpanningTree.md) 与 [堆](Heap.md)。
