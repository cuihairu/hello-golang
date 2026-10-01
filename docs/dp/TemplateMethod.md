### 模板方法模式 (Template Method Pattern)

#### 意图
模板方法模式是一种行为型设计模式，它在一个方法中定义一个操作的算法骨架，将一些步骤延迟到子类中实现。模板方法模式使得子类可以重定义算法的某些特定步骤，而不改变算法的整体结构。这个模式用于让子类在不改变算法结构的情况下，重新定义算法的某些特定步骤。

#### 问题
在现实世界中，考虑一个报表生成系统，生成报表的过程包括数据获取、数据处理和报表输出等多个步骤。不同类型的报表可能有不同的数据获取和处理方式，但整体流程是相同的。如果将整个报表生成流程都写在一个类中，会导致类变得复杂且难以维护。模板方法模式允许我们在基类中定义报表生成的算法骨架，并将具体的数据获取和处理步骤推迟到子类中实现，从而简化了报表生成流程的管理。

#### 解决方案
使用模板方法模式，我们可以在基类中定义一个模板方法，该方法包含了算法的整体结构，并调用一些可以被子类重写的钩子方法。具体的步骤由子类实现。基类保证了算法的骨架不被改变，而子类则提供了具体的实现细节。

#### 模式结构
1. **抽象类（Abstract Class）**：定义模板方法，并实现模板方法中的部分步骤。声明钩子方法，子类可以重写这些方法以提供具体实现。
2. **具体类（Concrete Class）**：继承抽象类，并实现抽象类中声明的钩子方法，提供具体的步骤实现。

#### 代码
以下是使用Go语言实现的模板方法模式示例：

```go
package main

import "fmt"

// 抽象类 - 报表生成
type ReportGenerator struct{}

// 模板方法 - 定义算法骨架
func (r *ReportGenerator) GenerateReport() {
    r.FetchData()
    r.ProcessData()
    r.OutputReport()
}

// 钩子方法 - 数据获取，子类可以重写
func (r *ReportGenerator) FetchData() {
    fmt.Println("获取数据")
}

// 钩子方法 - 数据处理，子类可以重写
func (r *ReportGenerator) ProcessData() {
    fmt.Println("处理数据")
}

// 钩子方法 - 报表输出，子类可以重写
func (r *ReportGenerator) OutputReport() {
    fmt.Println("输出报表")
}

// 具体类 - 销售报表生成
type SalesReportGenerator struct {
    ReportGenerator
}

func (r *SalesReportGenerator) FetchData() {
    fmt.Println("获取销售数据")
}

func (r *SalesReportGenerator) ProcessData() {
    fmt.Println("处理销售数据")
}

func (r *SalesReportGenerator) OutputReport() {
    fmt.Println("输出销售报表")
}

// 具体类 - 财务报表生成
type FinancialReportGenerator struct {
    ReportGenerator
}

func (r *FinancialReportGenerator) FetchData() {
    fmt.Println("获取财务数据")
}

func (r *FinancialReportGenerator) ProcessData() {
    fmt.Println("处理财务数据")
}

func (r *FinancialReportGenerator) OutputReport() {
    fmt.Println("输出财务报表")
}

func main() {
    // 创建销售报表生成器
    salesReport := &SalesReportGenerator{}
    salesReport.GenerateReport()

    // 创建财务报表生成器
    financialReport := &FinancialReportGenerator{}
    financialReport.GenerateReport()
}
```

#### 适用场景
- 当多个子类有相同的算法骨架，而只有部分步骤需要不同实现时。
- 当要在基类中定义算法的结构，同时允许子类提供具体实现时。
- 当实现代码重复且多次出现相同的算法结构时，模板方法模式可以减少代码重复。

#### 实现方式
1. 定义一个抽象类，包含模板方法和一些可以被子类重写的钩子方法。
2. 实现具体的子类，重写抽象类中的钩子方法，提供特定的实现。
3. 客户端代码使用抽象类定义的模板方法来执行算法，子类提供具体的实现细节。

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