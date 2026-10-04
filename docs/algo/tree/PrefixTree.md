# 前缀树

前缀树（Prefix Tree，又称 Trie、字典树）把字符串集合组织成一棵多叉树：从根到任意节点的路径拼起来就是一个前缀，约定前缀的终点节点标记"完整单词"。它让"按前缀查找"与"判断单词是否出现"在 $O(\text{长度})$ 时间内完成，与词表大小无关。

### 结构定义

1. **节点**: 每个节点的 `children` 用字符索引下一层节点（实现上可用数组、哈希表或有序数组）。
2. **路径即前缀**: 根到节点的边序列就是该节点代表的前缀。
3. **结束标记 `isEnd`**: 标记从根到该节点的路径构成一个完整插入过的单词。

### 核心操作

1. **Insert**: 逐字符下行，缺失就创建节点，末尾标记 `isEnd`。
2. **Search**: 逐字符下行走完，检查末节点是否 `isEnd`。
3. **StartsWith**: 逐字符下行走完即可，不要求 `isEnd`——这正是前缀查询。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// TrieNode 前缀树节点
type TrieNode struct {
	children map[byte]*TrieNode
	isEnd    bool
}

func newTrieNode() *TrieNode {
	return &TrieNode{children: make(map[byte]*TrieNode)}
}

// Trie 前缀树
type Trie struct {
	root *TrieNode
}

// NewTrie 创建空前缀树
func NewTrie() *Trie {
	return &Trie{root: newTrieNode()}
}

// Insert 插入单词
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

// Search 查找完整单词
func (t *Trie) Search(word string) bool {
	return t.walk(word, false)
}

// StartsWith 判断是否存在以 prefix 为前缀的单词
func (t *Trie) StartsWith(prefix string) bool {
	return t.walk(prefix, true)
}

// walk 下行匹配；prefixOnly 为 true 时不要求末尾是完整单词
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

运行输出：

```text
search go: true
search gox: false
startsWith go: true
startsWith co: true
startsWith codex: false
startsWith z: false
```

### 复杂度分析

- **Insert / Search / StartsWith**: $O(L)$，$L$ 为字符串长度（与词表大小无关）。
- **空间**: 最坏 $O(\sum L)$，共享公共前缀后通常远小于逐串存储；节点数过多时可用压缩（Patricia 树）优化。

### 应用场景

- 自动补全、拼写检查、敏感词过滤。
- IP 路由表最长前缀匹配、单词游戏（Boggle、Crossword）。

### 总结

前缀树把字符串的公共前缀共享成同一条路径，查找退化为逐字符下行。字符串索引类问题常从它入手，后缀树等结构也建立在类似思路上。
