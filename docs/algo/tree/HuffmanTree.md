# Huffman Tree

A Huffman tree is the optimal binary tree: given a set of leaves weighted by (occurrence) frequency, the Huffman tree is the binary tree that minimizes $\sum w_i \times l_i$ (the weighted path length), where $l_i$ is the depth of a leaf. Placing high-frequency characters closer to the root yields the optimal prefix code — Huffman coding, a basic building block of compression algorithms such as DEFLATE.

### Construction Steps (Greedy)

1. Count the frequency of each character; each character starts as a single-node tree and is inserted into a priority queue.
2. Take out the two trees with the smallest frequencies and merge them into a new tree (its root frequency is the sum of the two), then put it back into the queue.
3. Repeat until only one tree is left in the queue — that is the Huffman tree.
4. The path from the root to each leaf (left = 0, right = 1) is that character's Huffman code.

Since no character ever lies on another character's coding path, Huffman coding is a prefix code (no code is a prefix of another), so codes can be concatenated and decoded unambiguously.

### Code Example (Go Implementation)

```go
package main

import (
	"container/heap"
	"fmt"
)

// huffmanNode is a Huffman tree node
type huffmanNode struct {
	weight      int
	ch          byte // used by leaf nodes only
	left, right *huffmanNode
}

// priorityQueue is a min-priority queue
type priorityQueue []*huffmanNode

func (q priorityQueue) Len() int            { return len(q) }
func (q priorityQueue) Less(i, j int) bool  { return q[i].weight < q[j].weight }
func (q priorityQueue) Swap(i, j int)       { q[i], q[j] = q[j], q[i] }
func (q *priorityQueue) Push(x any)         { *q = append(*q, x.(*huffmanNode)) }
func (q *priorityQueue) Pop() any {
	old := *q
	n := len(old)
	item := old[n-1]
	*q = old[:n-1]
	return item
}

// buildHuffman builds a Huffman tree from the text
func buildHuffman(text string) *huffmanNode {
	freq := map[byte]int{}
	for i := 0; i < len(text); i++ {
		freq[text[i]]++
	}
	q := &priorityQueue{}
	for ch, w := range freq {
		*q = append(*q, &huffmanNode{weight: w, ch: ch})
	}
	heap.Init(q)
	for q.Len() > 1 {
		a := heap.Pop(q).(*huffmanNode)
		b := heap.Pop(q).(*huffmanNode)
		heap.Push(q, &huffmanNode{weight: a.weight + b.weight, left: a, right: b})
	}
	return heap.Pop(q).(*huffmanNode)
}

// collectCodes recursively collects the code of each leaf (character)
func collectCodes(n *huffmanNode, path string, out map[byte]string) {
	if n.left == nil && n.right == nil {
		out[n.ch] = path
		return
	}
	collectCodes(n.left, path+"0", out)
	collectCodes(n.right, path+"1", out)
}

func main() {
	text := "abbcccdddd"
	root := buildHuffman(text)

	codes := map[byte]string{}
	collectCodes(root, "", codes)
	for ch, code := range codes {
		fmt.Printf("%c -> %s\n", ch, code)
	}

	// compute the total bits after encoding, and compare with ASCII's 8-bit fixed-length coding
	bits := 0
	for i := 0; i < len(text); i++ {
		bits += len(codes[text[i]])
	}
	fmt.Printf("total bits of Huffman coding: %d (fixed-length coding needs %d bits)\n", bits, len(text)*8)
}
```

Output (with equal frequencies the code shapes may differ, but the total bit count is fixed):

```text
d -> 0
c -> 10
a -> 110
b -> 111
total bits of Huffman coding: 19 (fixed-length coding needs 80 bits)
```

### Complexity Analysis

Let $k$ be the number of distinct characters:

- **Construction**: $O(k \log k)$, with $k-1$ merges in total, each heap operation $O(\log k)$.
- **Encoding/decoding**: encoding first walks the tree in $O(k)$ to collect the code table, then generates the result in $O(n)$; decoding walks down the tree at $O(l)$ per character.
- **Space**: $O(k)$.

### Summary

The Huffman tree proves by a greedy strategy that "the higher the frequency, the closer to the root" minimizes the weighted path length, and its code is a prefix code that can be decoded on the fly. It is the classic construction of the optimal prefix code, and a good example for understanding correctness proofs of greedy algorithms.

## References

- [Huffman coding · Wikipedia](https://en.wikipedia.org/wiki/Huffman_coding)

## Sibling pages

- [Heap](/algo/tree/Heap.md)
- [MinimumSpanningTree](/algo/tree/MinimumSpanningTree.md)
- [RedBlackTree](/algo/tree/RedBlackTree.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Heap](/algo/tree/Heap.md)
