# Prefix Tree

A prefix tree (also called a Trie or dictionary tree) organizes a set of strings into a multi-way tree: the path from the root to any node, read together, is a prefix, and the node where a prefix ends is marked as a "complete word." This makes "lookup by prefix" and "is this word present" both finish in $O(\text{length})$ time, regardless of the dictionary size.

### Structure Definition

1. **Node**: each node's `children` indexes the next level of nodes by character (implemented with an array, a hash map, or a sorted array).
2. **Path is the prefix**: the sequence of edges from the root to a node is the prefix that node represents.
3. **End marker `isEnd`**: marks that the path from the root to this node forms a complete word that was inserted.

### Core Operations

1. **Insert**: walk down character by character, creating nodes where they are missing, then mark `isEnd` at the end.
2. **Search**: walk down character by character all the way through, then check whether the final node has `isEnd`.
3. **StartsWith**: just walk down character by character all the way through, without requiring `isEnd` — this is exactly the prefix query.

### Code Example (Go Implementation)

```go
package main

import "fmt"

// TrieNode prefix tree node
type TrieNode struct {
	children map[byte]*TrieNode
	isEnd    bool
}

func newTrieNode() *TrieNode {
	return &TrieNode{children: make(map[byte]*TrieNode)}
}

// Trie prefix tree
type Trie struct {
	root *TrieNode
}

// NewTrie creates an empty prefix tree
func NewTrie() *Trie {
	return &Trie{root: newTrieNode()}
}

// Insert adds a word
func (t *Trie) Insert(word string) {
	cur := t.root
	for i := 0; i < len(word); i++ {
		c := word[i]
		next, ok := cur.children[c]
		if !ok {
			next = newTrieNode()
			cur.children[c] = next
		}
		cur = next
	}
	cur.isEnd = true
}

// Search looks up a complete word
func (t *Trie) Search(word string) bool {
	return t.walk(word, false)
}

// StartWith reports whether a word starts with prefix
func (t *Trie) StartsWith(prefix string) bool {
	return t.walk(prefix, true)
}

// walk descends and matches; when prefixOnly is true the end need not be a complete word
func (t *Trie) walk(s string, prefixOnly bool) bool {
	cur := t.root
	for i := 0; i < len(s); i++ {
		next, ok := cur.children[s[i]]
		if !ok {
			return false
		}
		cur = next
	}
	return prefixOnly || cur.isEnd
}

func main() {
	trie := NewTrie()
	for _, w := range []string{"go", "golang", "code", "coder"} {
		trie.Insert(w)
	}

	fmt.Println("search go:", trie.Search("go"))
	fmt.Println("search gox:", trie.Search("gox"))
	fmt.Println("startsWith go:", trie.StartsWith("go"))
	fmt.Println("startsWith co:", trie.StartsWith("co"))
	fmt.Println("startsWith codex:", trie.StartsWith("codex"))
	fmt.Println("startsWith z:", trie.StartsWith("z"))
}
```

Output:

```text
search go: true
search gox: false
startsWith go: true
startsWith co: true
startsWith codex: false
startsWith z: false
```

### Complexity Analysis

- **Insert / Search / StartsWith**: $O(L)$, where $L$ is the string length (independent of the dictionary size).
- **Space**: worst case $O(\sum L)$; after sharing common prefixes it is usually much smaller than storing each string separately; when the node count grows large, use compression (Patricia tree) to optimize.

### Application Scenarios

- Auto-completion, spell checking, sensitive word filtering.
- Longest prefix matching for IP routing tables, word games (Boggle, Crossword).

### Summary

A prefix tree shares the common prefix of strings along a single path, so lookup degrades to walking down character by character. Problems involving string indexing often start here, and suffix trees and similar structures are built on the same idea.

## References

- [Prefix Tree (Trie) · Wikipedia](https://en.wikipedia.org/wiki/Trie)

## Sibling pages

- [Heap](/algo/tree/Heap.md)
- [MinimumSpanningTree](/algo/tree/MinimumSpanningTree.md)
- [RedBlackTree](/algo/tree/RedBlackTree.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Heap](/algo/tree/Heap.md)
