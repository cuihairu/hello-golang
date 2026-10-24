### Graph

A graph consists of vertices and edges and describes "many-to-many" relationships: friendships in a social network, the ordering of dependent tasks, network routing — all take the form of a graph. The [minimum spanning tree](/algo/tree/MinimumSpanningTree.md) page in the tree section covers classic algorithms on weighted graphs; this page covers graph representation and the two traversals.

### Adjacency-list representation

The most common representation in Go is a `map` plus slices: each vertex maps to its list of neighbors. Edges of an undirected graph must be registered twice:

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

When vertex IDs are dense, use a `[][]int` slice instead of a `map` for faster access; for a weighted graph, replace the neighbors with a struct (vertex + weight).

### Traversal: BFS and DFS

Breadth-first search (BFS) spreads level by level and uses a queue; depth-first search (DFS) walks one path to the end and uses a stack (or recursion). Both rely on a `visited` set to avoid looping around:

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

	fmt.Println("BFS from 0:", g.BFS(0)) // prints: BFS from 0: [0 1 2 3 4]
	fmt.Println("DFS from 0:", g.DFS(0)) // prints: DFS from 0: [0 1 3 2 4]
}
```

Both traversals are O(V+E): every vertex enters and leaves the container once, and every edge is examined twice.

### How to choose

- **Shortest path in an unweighted graph, level-order problems** → BFS; the first time you reach a vertex is already the shortest path to it.
- **Connectivity, cycle detection, problems that need backtracking** (topological sort, mazes) → DFS.
- The recursive form of DFS is shorter, but the depth may exceed the stack limit; the explicit-stack version has no such worry.

### Summary

An adjacency list with a `map` is the basic setup for representing graphs in Go; a queue for BFS, a stack for DFS, and the `visited` set is the key to preventing loops. For shortest paths and minimum spanning trees on weighted graphs, see [minimum spanning tree](/algo/tree/MinimumSpanningTree.md) and [heap](/algo/tree/Heap.md).

## References

- [Graph (abstract data type) · Wikipedia](https://en.wikipedia.org/wiki/Graph_%28abstract_data_type%29))
- [Graph theory · Wikipedia](https://en.wikipedia.org/wiki/Graph_theory)

## Sibling pages

- [Inventory](/algo/Inventory.md)
- [Queue](/algo/queue/Queue.md)
- [Stack](/algo/stack/Stack.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Inventory](/algo/Inventory.md)
- [Queue](/algo/queue/Queue.md)
- [Stack](/algo/stack/Stack.md)
