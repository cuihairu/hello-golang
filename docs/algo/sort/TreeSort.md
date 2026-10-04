**树排序（Tree Sort）**

树排序是一种基于树数据结构的排序算法，主要利用二叉搜索树（BST）或其变种（如 AVL 树、红黑树等）来实现排序。其基本思想是将待排序的元素插入到一个二叉搜索树中，然后通过中序遍历树来获得有序的元素序列。

### 1. 算法概念

树排序的核心思想是：
1. **构建二叉搜索树**: 将待排序的元素逐一插入到二叉搜索树中。
2. **中序遍历**: 通过中序遍历二叉搜索树，可以按升序输出所有元素，从而实现排序。

### 2. 算法步骤

1. **构建二叉搜索树**: 把输入数组的元素逐一插入，插入遵循 BST 的性质：左子树的所有节点值小于根节点值，右子树的所有节点值大于根节点值。
2. **中序遍历**: 按左子树、根节点、右子树的顺序访问整棵树，输出天然按升序排列。

### 3. 时间复杂度和空间复杂度

- **时间复杂度**: 树是平衡的（如 AVL 树、红黑树）时为 $O(n \log n)$，随机插入平均也是 $O(n \log n)$；插入顺序恰好升序或降序时树退化成链表，掉到 $O(n^2)$。
- **空间复杂度**: $O(n)$，需要额外的空间来存储二叉搜索树的节点。

### 4. 代码示例

```go
package main

import "fmt"

// 定义二叉搜索树节点
type TreeNode struct {
    value int
    left  *TreeNode
    right *TreeNode
}

// 插入节点到二叉搜索树
func insert(root *TreeNode, value int) *TreeNode {
    if root == nil {
        return &TreeNode{value: value}
    }
    if value < root.value {
        root.left = insert(root.left, value)
    } else {
        root.right = insert(root.right, value)
    }
    return root
}

// 中序遍历二叉搜索树
func inorderTraversal(root *TreeNode, result *[]int) {
    if root != nil {
        inorderTraversal(root.left, result)
        *result = append(*result, root.value)
        inorderTraversal(root.right, result)
    }
}

// 树排序
func treeSort(arr []int) []int {
    if len(arr) == 0 {
        return arr
    }

    var root *TreeNode
    for _, value := range arr {
        root = insert(root, value)
    }

    var sorted []int
    inorderTraversal(root, &sorted)
    return sorted
}

func main() {
    arr := []int{5, 3, 8, 1, 4, 7, 9}
    fmt.Println("Original array:", arr)
    sorted := treeSort(arr)
    fmt.Println("Sorted array:", sorted)
}
```

### 5. 优缺点

树排序思路直接：建树、中序遍历，两步就出有序序列。短板在树的形状不受控——插入顺序不巧时树退化成链表，效率掉到 $O(n^2)$；另外每个元素都要一个节点，$O(n)$ 的额外空间省不掉。要稳就得用 AVL、红黑树这类自平衡变种。

### 总结

树排序把排序交给二叉搜索树：元素逐个插入建树，中序遍历一遍就是升序序列。树平衡时是 $O(n \log n)$，退化时是 $O(n^2)$，所以用不用它，先看数据能不能保证树不歪。