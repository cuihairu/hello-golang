# 表达式树

表达式树（Expression Tree）是把表达式按运算优先级组织成的二叉树：叶子节点是操作数，内部节点是运算符，左子树是左操作数对应的子表达式，右子树是右操作数。编译器、计算器引擎都借助它来表示和求值表达式。

### 三种遍历对应三种表示

| 遍历方式 | 输出形式 |
| -------- | -------- |
| 中序遍历 | 中缀表达式（需要括号） |
| 前序遍历 | 前缀表达式（波兰式） |
| 后序遍历 | 后缀表达式（逆波兰式） |

### 算法步骤（由后缀表达式构建）

1. 从左到右扫描后缀表达式（逆波兰式）的每个记号。
2. 遇到操作数：创建叶子节点压栈。
3. 遇到运算符：弹出栈顶两个节点，先弹出的是右操作数，后弹出的是左操作数，组合成新的内部节点后压栈。
4. 扫描结束后栈中唯一节点即根节点。

### 代码示例（Go语言实现）

```go
package main

import (
	"fmt"
	"strconv"
)

// ExprNode 表达式树节点
type ExprNode struct {
	Val   string
	Left  *ExprNode
	Right *ExprNode
}

// isOperator 判断是否为四则运算符
func isOperator(tok string) bool {
	return tok == "+" || tok == "-" || tok == "*" || tok == "/"
}

// buildExpressionTree 由后缀表达式构建表达式树
func buildExpressionTree(postfix []string) *ExprNode {
	stack := []*ExprNode{}
	for _, tok := range postfix {
		if isOperator(tok) {
			right := stack[len(stack)-1]
			left := stack[len(stack)-2]
			stack = stack[:len(stack)-2]
			stack = append(stack, &ExprNode{Val: tok, Left: left, Right: right})
		} else {
			stack = append(stack, &ExprNode{Val: tok})
		}
	}
	return stack[0]
}

// eval 递归求值
func eval(n *ExprNode) int {
	if !isOperator(n.Val) {
		v, _ := strconv.Atoi(n.Val)
		return v
	}
	l, r := eval(n.Left), eval(n.Right)
	switch n.Val {
	case "+":
		return l + r
	case "-":
		return l - r
	case "*":
		return l * r
	default:
		return l / r
	}
}

// infix 中序遍历，输出带括号的中缀形式
func infix(n *ExprNode) string {
	if !isOperator(n.Val) {
		return n.Val
	}
	return "(" + infix(n.Left) + " " + n.Val + " " + infix(n.Right) + ")"
}

// postfix 后序遍历，输出后缀形式
func postfix(n *ExprNode, out *[]string) {
	if n == nil {
		return
	}
	postfix(n.Left, out)
	postfix(n.Right, out)
	*out = append(*out, n.Val)
}

func main() {
	// (3+4)*2/7 的后缀表达式
	tokens := []string{"3", "4", "+", "2", "*", "7", "/"}
	root := buildExpressionTree(tokens)

	fmt.Println("中缀形式:", infix(root))
	fmt.Println("求值结果:", eval(root))

	var out []string
	postfix(root, &out)
	fmt.Println("后缀形式:", out)
}
```

运行输出：

```text
中缀形式: (((3 + 4) * 2) / 7)
求值结果: 2
后缀形式: [3 4 + 2 * 7 /]
```

### 复杂度分析

- **构建**: $O(n)$，每个记号入栈出栈一次。
- **求值/遍历**: $O(n)$，每个节点访问一次。
- **空间**: $O(n)$ 栈与节点，递归深度 $O(h)$。

### 总结

表达式树把"运算优先级"写进了树形结构，求值就是一次后序遍历。构建用的"后缀表达式 + 栈"，编译器的表达式分析和计算器实现都在用。
