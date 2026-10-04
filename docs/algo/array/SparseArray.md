# 稀疏数组

稀疏数组（Sparse Array）是一种压缩存储方式，用于保存大量元素为零（或同一默认值）的二维数组。它只记录"非零元素的坐标和值"，把 $m \times n$ 的存储换成 $k+1$ 行三元组。

### 算法概述

1. **统计**: 扫描原数组，统计非零元素的个数 `sum`。
2. **建立稀疏数组**: 稀疏数组是一个 `(sum+1) × 3` 的表，第 0 行记录原数组的行数、列数和非零元素个数，之后每行记录一个非零元素的 `行、列、值` 三元组。
3. **还原**: 读取第 0 行恢复原数组尺寸，再逐行把非零元素填回对应坐标。

### 算法步骤

1. **压缩**:
   - 遍历原二维数组，收集所有非零元素到三元组列表。

2. **还原**:
   - 按第 0 行的行列数创建新数组并全部置零。
   - 遍历三元组，执行 `arr[row][col] = value`。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// toSparse 把二维数组压缩为稀疏数组
func toSparse(arr [][]int) [][]int {
	sum := 0
	for _, row := range arr {
		for _, v := range row {
			if v != 0 {
				sum++
			}
		}
	}
	sparse := make([][]int, sum+1)
	sparse[0] = []int{len(arr), len(arr[0]), sum}
	idx := 1
	for i, row := range arr {
		for j, v := range row {
			if v != 0 {
				sparse[idx] = []int{i, j, v}
				idx++
			}
		}
	}
	return sparse
}

// fromSparse 把稀疏数组还原为二维数组
func fromSparse(sparse [][]int) [][]int {
	rows, cols := sparse[0][0], sparse[0][1]
	arr := make([][]int, rows)
	for i := range arr {
		arr[i] = make([]int, cols)
	}
	for _, item := range sparse[1:] {
		arr[item[0]][item[1]] = item[2]
	}
	return arr
}

func main() {
	arr := [][]int{
		{0, 0, 3, 0, 0},
		{0, 5, 0, 0, 0},
		{0, 0, 0, 0, 0},
		{7, 0, 0, 2, 0},
	}
	sparse := toSparse(arr)
	fmt.Println("稀疏数组:")
	for _, row := range sparse {
		fmt.Println(row)
	}

	restored := fromSparse(sparse)
	fmt.Println("还原后的数组:")
	for _, row := range restored {
		fmt.Println(row)
	}
}
```

运行输出：

```text
稀疏数组:
[4 5 4]
[0 2 3]
[1 1 5]
[3 0 7]
[3 3 2]
还原后的数组:
[0 0 3 0 0]
[0 5 0 0 0]
[0 0 0 0 0]
[7 0 0 2 0]
```

### 复杂度分析

设原数组为 $m \times n$，非零元素个数为 $k$：

- **压缩**: 时间 $O(mn)$，空间 $O(k)$。
- **还原**: 时间 $O(mn + k)$，空间 $O(mn)$。
- 当 $k \ll mn$ 时，稀疏数组的存储量远小于原数组。

### 应用场景

- 棋盘、地图等大面积空白的数据存储。
- 稀疏矩阵的存储与运算（如图的邻接矩阵）。

### 总结

稀疏数组用"坐标 + 值"的三元组记录少量有效数据，用 $O(k)$ 的空间换掉 $O(mn)$ 的存储，棋盘存档和稀疏矩阵存储是它的典型场景。
