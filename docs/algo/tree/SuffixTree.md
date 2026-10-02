# 后缀树

后缀树（Suffix Tree）是把一个字符串的**所有后缀**组织起来的压缩 Trie：从根到任意叶子的路径对应原串的一个后缀，公共后缀被共享。有了它，子串查找、重复子串发现、最长重复子串等问题都可以在与模式长度成正比的时间内完成。

### 结构定义

1. **后缀**: `s[i..n-1]`，共 $n$ 个（含空前缀）。
2. **共享前缀**: 两个后缀的公共前缀（即原串的公共子串）在树中共享同一条路径。
3. **压缩边**: 生产级后缀树把只有单个孩子的链压成一条边上带起止下标的边（隐含中间字符），空间降为 $O(n)$；Ukkonen 算法可在 $O(n)$ 时间在线性空间内构建。

### 算法步骤（朴素构建 + 查询）

1. **构建**: 对 $i = 0..n-1$，把后缀 `s[i..]` 逐字符插入 Trie，缺失的节点就新建——这是 $O(n^2)$ 的朴素实现，适合教学与小字符串。
2. **子串查询**: 沿树逐字符匹配模式串，任何一步没有对应孩子即失败；走完即说明该子串出现过。
3. **出现位置**: 叶子的下标集合即所有出现起始位置（压缩版通过遍历子树收集）。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// suffixNode 后缀树节点（未压缩版本，边为单字符）
type suffixNode struct {
	children map[byte]*suffixNode
	// idx 仅在叶子上记录该后缀的起始下标，-1 表示中间节点
	idx int
}

// buildSuffixTree 朴素构建后缀树，O(n^2)
func buildSuffixTree(s string) *suffixNode {
	root := &suffixNode{children: make(map[byte]*suffixNode), idx: -1}
	for i := 0; i < len(s); i++ {
		cur := root
		for j := i; j < len(s); j++ {
			c := s[j]
			next, ok := cur.children[c]
			if !ok {
				next = &suffixNode{children: make(map[byte]*suffixNode), idx: -1}
				cur.children[c] = next
			}
			cur = next
		}
		cur.idx = i // 叶子记录后缀起点
	}
	return root
}

// contains 查询子串是否出现
func contains(root *suffixNode, p string) bool {
	cur := root
	for i := 0; i < len(p); i++ {
		next, ok := cur.children[p[i]]
		if !ok {
			return false
		}
		cur = next
	}
	return true
}

// occurrences 返回子串所有出现的起始下标
func occurrences(root *suffixNode, p string) []int {
	cur := root
	for i := 0; i < len(p); i++ {
		next, ok := cur.children[p[i]]
		if !ok {
			return nil
		}
		cur = next
	}
	var out []int
	var collect func(n *suffixNode)
	collect = func(n *suffixNode) {
		// 未压缩的后缀树中，一个节点可能既是某后缀的终点又有孩子
		//（该后缀是其他后缀的前缀），因此不能提前返回
		if n.idx >= 0 {
			out = append(out, n.idx)
		}
		for _, c := range n.children {
			collect(c)
		}
	}
	collect(cur)
	// 简单排序输出（出现顺序不确定）
	for i := 0; i < len(out); i++ {
		for j := i + 1; j < len(out); j++ {
			if out[j] < out[i] {
				out[i], out[j] = out[j], out[i]
			}
		}
	}
	return out
}

func main() {
	s := "banana"
	root := buildSuffixTree(s)

	fmt.Println("包含 ana:", contains(root, "ana"))
	fmt.Println("包含 nan:", contains(root, "nan"))
	fmt.Println("包含 ananas:", contains(root, "ananas"))

	fmt.Println("ana 出现在:", occurrences(root, "ana"))
	fmt.Println("na 出现在:", occurrences(root, "na"))
}
```

运行输出：

```text
包含 ana: true
包含 nan: true
包含 ananas: false
ana 出现在: [1 3]
na 出现在: [2 4]
```

### 复杂度分析

- **朴素构建**: $O(n^2)$ 时间、$O(n^2)$ 最坏空间（本篇实现）。
- **子串查询**: $O(m)$，$m$ 为模式长度。
- **压缩版（Ukkonen）**: 构建 $O(n)$ 时间、$O(n)$ 空间，查询仍为 $O(m)$。

### 应用场景

- 子串匹配、最长重复子串、最长公共子串。
- 生物信息学序列比对、数据压缩中的重复片段发现。

### 总结

后缀树把"每个子串"化归为"某个后缀的前缀"，从而只需对后缀建索引即可覆盖全部子串查询。本篇的朴素版便于理解语义，工程上应使用压缩边 + Ukkonen 算法把构建降到线性。
