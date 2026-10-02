# 霍夫曼树

霍夫曼树（Huffman Tree）是最优二叉树：给定一组带权（出现频率）的叶子，霍夫曼树是使 $\sum w_i \times l_i$（带权路径长度）最小的二叉树，其中 $l_i$ 是叶子的深度。把高频字符放得离根更近，就得到了最优前缀编码——霍夫曼编码，它是压缩算法（如 DEFLATE）的基础部件。

### 构建步骤（贪心）

1. 统计每个字符的频率，每个字符先作为一棵单节点树入优先队列。
2. 取出频率最小的两棵树，合并为一棵新树（新根频率为两者之和），放回队列。
3. 重复直到队列只剩一棵树，即为霍夫曼树。
4. 从根到每个叶子的路径（左 0 右 1）即为该字符的霍夫曼编码。

由于任何字符都不在其他字符编码路径上，霍夫曼编码是前缀码（任何编码都不是另一个的前缀），可以无歧义地拼接解码。

### 代码示例（Go语言实现）

```go
package main

import (
	"container/heap"
	"fmt"
)

// huffmanNode 霍夫曼树节点
type huffmanNode struct {
	weight      int
	ch          byte // 仅叶节点使用
	left, right *huffmanNode
}

// priorityQueue 最小优先队列
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

// buildHuffman 根据文本构建霍夫曼树
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

// collectCodes 递归收集每个叶子（字符）的编码
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

	// 计算编码后的总位数，并与 ASCII 的 8 位定长编码比较
	bits := 0
	for i := 0; i < len(text); i++ {
		bits += len(codes[text[i]])
	}
	fmt.Printf("霍夫曼编码总位数: %d（定长编码需要 %d 位）\n", bits, len(text)*8)
}
```

运行输出（相同频率时编码形态可能不同，总位数固定）：

```text
d -> 0
c -> 10
a -> 110
b -> 111
霍夫曼编码总位数: 19（定长编码需要 80 位）
```

### 复杂度分析

设字符种数为 $k$：

- **构建**: $O(k \log k)$，共 $k-1$ 次合并，每次堆操作 $O(\log k)$。
- **编码/解码**: 编码需先遍历树 $O(k)$ 收集码表，随后 $O(n)$ 生成；解码沿树下行每个字符 $O(l)$。
- **空间**: $O(k)$。

### 总结

霍夫曼树用贪心策略证明了"频率越高离根越近"能使带权路径长度最小，其编码是可即时解码的前缀码。它是最优前缀编码的经典构造，也是理解贪心算法正确性证明的范例。
