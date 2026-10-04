# 后缀数组

后缀数组（Suffix Array）把字符串的所有后缀按字典序排序，记录"第 $i$ 小的后缀的起始下标"。它与后缀树功能等价，但只是两个整数数组，空间和实现成本都小得多，是字符串处理（重复子串、模式匹配、LCP）的主力结构。

### 定义

1. **后缀数组 `sa`**: `sa[i]` = 按字典序第 $i$ 小的后缀的起始下标。
2. **排名数组 `rank`**: `rank` 是 `sa` 的逆，`rank[j]` = 后缀 `j` 的字典序名次，`sa[rank[j]] = j`。
3. **倍增法**: 以长度 $k$ 的排名为基础，用 `(rank[i], rank[i+k])` 二元组排序得到长度 $2k$ 的排名，$\log n$ 轮后所有后缀排名互异。

### 算法步骤（倍增法）

1. 初始按单个字符赋排名。
2. 每轮按 `(rank[i], rank[i+k])`（越界记为 $-1$，排最前）对所有起点排序，重算排名。
3. 若所有排名已互异则结束，否则倍增 $k$。

### 代码示例（Go语言实现）

```go
package main

import (
	"fmt"
	"sort"
)

// buildSuffixArray 倍增法构建后缀数组，O(n log^2 n)
func buildSuffixArray(s string) []int {
	n := len(s)
	if n == 0 {
		return nil
	}
	sa := make([]int, n)
	rank := make([]int, n)
	tmp := make([]int, n)
	for i := 0; i < n; i++ {
		sa[i] = i
		rank[i] = int(s[i])
	}
	for k := 1; ; k *= 2 {
		less := func(i, j int) bool { // 后缀 i 是否排在 j 前
			if rank[i] != rank[j] {
				return rank[i] < rank[j]
			}
			ri, rj := -1, -1
			if i+k < n {
				ri = rank[i+k]
			}
			if j+k < n {
				rj = rank[j+k]
			}
			return ri < rj
		}
		sort.Slice(sa, func(a, b int) bool { return less(sa[a], sa[b]) })
		tmp[sa[0]] = 0
		for i := 1; i < n; i++ {
			tmp[sa[i]] = tmp[sa[i-1]]
			if less(sa[i-1], sa[i]) {
				tmp[sa[i]]++
			}
		}
		rank, tmp = tmp, rank // 新排名写入 rank，tmp 复用为缓冲
		if rank[sa[n-1]] == n-1 {
			break // 所有后缀排名互异，排序完成
		}
	}
	return sa
}

func main() {
	s := "banana"
	sa := buildSuffixArray(s)
	fmt.Println("后缀数组:", sa)
	for _, i := range sa {
		fmt.Printf("%d: %s\n", i, s[i:])
	}
}
```

运行输出：

```text
后缀数组: [5 3 1 0 4 2]
5: a
3: ana
1: anana
0: banana
4: na
2: nana
```

### 复杂度分析

- **构建**: $O(n \log^2 n)$（每轮一次比较排序）；改用基数排序可到 $O(n \log n)$，SA-IS 算法可到 $O(n)$。
- **空间**: $O(n)$。
- **子串匹配**: 结合二分与 LCP 数组，$O(m \log n)$。

### 应用场景

- 最长重复子串、不同子串计数（配合高度数组）。
- 全文检索、压缩（BWT 变换基于后缀数组）、生物序列分析。

### 总结

后缀数组用"排序所有后缀"这一简单语义换来了与后缀树同级的表达能力，而实现只有几十行。倍增法最容易理解：每轮排名都由上一轮排名按位扩展而来。
