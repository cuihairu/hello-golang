### 区间树排序（Interval Tree Sort）

**区间树排序**（Interval Tree Sort）把待排序的数当成退化区间 `[x, x]` 插进区间树，再中序遍历取出有序序列。区间树是一棵带 `max` 字段的二叉搜索树，用来回答区间重叠、区间查询这类问题。

### 区间树概述

区间树是一种用于存储区间数据的数据结构，它支持以下操作：

1. **插入**: 将一个新的区间插入到区间树中。
2. **删除**: 从区间树中删除一个区间。
3. **查询**: 查找与给定区间有重叠的所有区间。

### 区间树排序算法

区间树排序只有两步：

1. **构建区间树**:
   - 每个数据点当作区间 `[x, x]` 插入，`x` 就是数据点的值。

2. **中序遍历**:
   - 按左子树、根、右子树的顺序读出节点，得到的就是有序序列。

### 代码示例（Go语言实现）

下面是区间树的 Go 实现和排序示例：

```go
package main

import "fmt"

// 区间树节点
type IntervalTreeNode struct {
    start   int
    end     int
    max     int
    left    *IntervalTreeNode
    right   *IntervalTreeNode
}

// 创建新的区间树节点
func newIntervalTreeNode(start, end int) *IntervalTreeNode {
    return &IntervalTreeNode{
        start: start,
        end:   end,
        max:   end,
    }
}

// 插入节点到区间树
func insert(root *IntervalTreeNode, node *IntervalTreeNode) *IntervalTreeNode {
    if root == nil {
        return node
    }

    if node.start < root.start {
        root.left = insert(root.left, node)
    } else {
        root.right = insert(root.right, node)
    }

    if root.max < node.end {
        root.max = node.end
    }

    return root
}

// 中序遍历区间树
func inorderTraversal(root *IntervalTreeNode, result *[]int) {
    if root != nil {
        inorderTraversal(root.left, result)
        *result = append(*result, root.start)
        inorderTraversal(root.right, result)
    }
}

// 区间树排序
func intervalTreeSort(arr []int) []int {
    var root *IntervalTreeNode
    for _, value := range arr {
        node := newIntervalTreeNode(value, value)
        root = insert(root, node)
    }

    var sortedArr []int
    inorderTraversal(root, &sortedArr)
    return sortedArr
}

func main() {
    arr := []int{38, 27, 43, 3, 9, 82, 10}
    sortedArr := intervalTreeSort(arr)
    fmt.Println("Sorted array:", sortedArr)
}
```

### 复杂度分析

- **时间复杂度**:
  - **构建区间树**: $O(n \log n)$，其中 $n$ 是待排序数据的数量。
  - **排序结果生成**: $O(n)$，通过中序遍历获取排序结果。

- **空间复杂度**: $O(n)$，用于存储区间树。

### 优缺点

- **优点**:
  - 插入按 `start` 走 BST 的比较，中序遍历直接给出有序序列，排序由遍历一步完成。
  - 节点上的 `max` 字段记录子树里的最大端点，做区间重叠查询时靠它剪枝。

- **缺点**:
  - 排序场景里每个数都退化成 `[x, x]`，区间重叠查询根本用不上，结构上的额外字段白带着。
  - 要维护 `max` 和左右子树，比直接比较数值多写插入、更新两段逻辑。

### 应用场景

拿区间树来排序，实际适合的只有一种情况：数据本来就是区间，插入之后还要反复做重叠查询，排序只是顺带的。单纯排序不需要区间树。

### 总结

区间树排序的全部动作是插树加中序遍历：`intervalTreeSort` 建树，`inorderTraversal` 读出有序序列。它的长处在区间重叠查询，纯粹排序用不着这棵树。