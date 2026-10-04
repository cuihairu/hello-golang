### 模板方法模式 (Template Method Pattern)

#### 意图
模板方法模式是一种行为型设计模式，在一个方法里定死算法的骨架，把其中某些步骤留给子类或注入的实现去填。子类换的只是个别步骤，整个流程的先后顺序不变。

#### 问题
在现实世界中，考虑一个报表生成系统，生成报表的过程包括数据获取、数据处理和报表输出等多个步骤。不同类型的报表可能有不同的数据获取和处理方式，但整体流程是相同的。如果将整个报表生成流程都写在一个类中，会导致类变得复杂且难以维护。模板方法模式允许我们在基类中定义报表生成的算法骨架，并将具体的数据获取和处理步骤推迟到子类中实现，从而简化了报表生成流程的管理。

#### 解决方案
在基类里定义模板方法，方法体按固定顺序调用几个钩子方法；钩子由子类重写或注入实现。骨架不被改动，变动的只有每一步的内容。

#### 模式结构
1. **抽象类（Abstract Class）**：定义模板方法（算法骨架），并声明可被替换的钩子步骤。
2. **具体类（Concrete Class）**：提供钩子步骤的具体实现，替换掉抽象类中的默认步骤。

#### 代码

```go
package main

import "fmt"

// ReportGenerator 是报表生成的"抽象类"，承载算法骨架。
// Go 没有继承，嵌入结构体的方法调用是静态分派，子类型里"重写"的方法不会被模板方法调用，
// 因此这里用函数字段来承载钩子步骤，由具体的报表类型在构造时注入自己的实现。
type ReportGenerator struct {
    fetch    func()
    process  func()
    output   func()
}

// GenerateReport 是模板方法 - 定义算法骨架
func (r *ReportGenerator) GenerateReport() {
    r.fetch()
    r.process()
    r.output()
}

// NewReportGenerator 使用默认步骤创建报表生成器
func NewReportGenerator(fetch, process, output func()) *ReportGenerator {
    return &ReportGenerator{fetch: fetch, process: process, output: output}
}

// 具体类 - 销售报表生成，注入销售报表的具体步骤
func NewSalesReportGenerator() *ReportGenerator {
    return NewReportGenerator(
        func() { fmt.Println("获取销售数据") },
        func() { fmt.Println("处理销售数据") },
        func() { fmt.Println("输出销售报表") },
    )
}

// 具体类 - 财务报表生成，注入财务报表的具体步骤
func NewFinancialReportGenerator() *ReportGenerator {
    return NewReportGenerator(
        func() { fmt.Println("获取财务数据") },
        func() { fmt.Println("处理财务数据") },
        func() { fmt.Println("输出财务报表") },
    )
}

func main() {
    // 创建销售报表生成器
    salesReport := NewSalesReportGenerator()
    salesReport.GenerateReport()

    // 创建财务报表生成器
    financialReport := NewFinancialReportGenerator()
    financialReport.GenerateReport()
}
```

输出：

```
获取销售数据
处理销售数据
输出销售报表
获取财务数据
处理财务数据
输出财务报表
```

#### 适用场景
- 当多个子类有相同的算法骨架，而只有部分步骤需要不同实现时。
- 当要在基类中定义算法的结构，同时允许子类提供具体实现时。
- 当实现代码重复且多次出现相同的算法结构时，模板方法模式可以减少代码重复。

#### 实现方式
1. 定义一个结构体，包含模板方法和承载钩子步骤的函数字段（或接口）。
2. 为每种具体报表提供构造函数，注入各自的钩子实现。
3. 客户端代码通过构造函数创建具体报表生成器，调用统一的模板方法执行算法。

#### 优缺点
**优点**：
- 通过将算法的骨架定义在基类中，可以避免代码重复，并使得算法结构清晰。
- 子类可以选择性地重写某些步骤，从而实现不同的变体。
- 易于扩展，添加新步骤或修改现有步骤不会影响已存在的子类。

**缺点**：
- 可能会导致基类和子类之间的紧耦合，因为子类依赖于基类的模板方法。
- 如果模板方法中包含复杂的逻辑，可能会导致基类过于庞大和复杂。

#### 其他模式的关系
- **模板方法模式与策略模式（Strategy Pattern）**：策略模式用于定义一系列算法并使其可以互换，而模板方法模式用于在基类中定义算法的骨架，并将某些步骤推迟到子类中实现。可以结合使用，例如在模板方法中使用策略模式来处理具体的步骤。
- **模板方法模式与工厂方法模式（Factory Method Pattern）**：工厂方法模式用于创建对象，而模板方法模式用于定义算法的骨架。可以结合使用，例如在模板方法中使用工厂方法模式来创建不同的对象。
- **模板方法模式与状态模式（State Pattern）**：状态模式用于根据对象的状态改变其行为，而模板方法模式用于在基类中定义算法的骨架。可以结合使用，例如在模板方法中使用状态模式来管理算法的步骤。