Idioms（惯用法）和 Patterns（模式）指编程语言里约定俗成的写法，用来解决常见问题。两者的边界并不严格：模式也可以泛指某种语言里反复出现的编程习惯。

### 相关术语解释

1. **Idioms**（惯用法/习惯用法）：
    - 特定语言中常见的、被广泛接受的写法和用法。
    - 简洁、有效地解决特定问题的写法。

2. **Patterns**（模式）：
    - 一般指软件设计模式，在特定上下文中反复出现的问题及其解决方案。
    - 更广泛地可以指特定语言中的常见编程模式和习惯用法。

### 相关示例

#### Idioms in Go
- **Comma ok idiom** for type assertions, map lookups, and channel receives.
- **Short variable declaration** using `:=`.
- **Blank identifier** (`_`) for ignoring values.
- **Defer** for resource management and cleanup.

#### Patterns in Go
- **Multiple return values** for error handling and results.
- **Named return values** for clarity and simplicity.
- **Type switch** for handling multiple types in a type-safe manner.
- **Select statement** for multiplexing on channels.
- **Anonymous functions and closures** for encapsulating behavior.

### 官方资源

- [Effective Go](https://go.dev/doc/effective_go)：Go 官方的惯用法和最佳实践指南。
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)：Go 代码审查评论，涵盖了许多惯用法和建议。

### 总结

Comma ok、`:=`、空白标识符 `_`、`defer`、多返回值、type switch 这些写法在 Effective Go 和 Go Code Review Comments 里都有说明。照这些惯例写，读代码的人不用猜你为什么这么写。