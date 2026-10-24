### Template Method Pattern

#### Intent
The Template Method pattern is a behavioral design pattern that fixes an algorithm's skeleton inside a single method and leaves some of the steps to be filled in by subclasses or by injected implementations. A subclass only changes individual steps; the order of the whole flow stays the same.

#### Problem
Consider a report generation system in the real world. Generating a report involves several steps such as fetching data, processing data, and outputting the report. Different types of reports may fetch and process data differently, but the overall flow is the same. Writing the whole report generation flow into one class makes that class complex and hard to maintain. The Template Method pattern lets us define the algorithm's skeleton for report generation in a base class and defer the concrete data-fetching and processing steps to subclasses, which simplifies managing the report generation flow.

#### Solution
Define the template method in the base class; its body calls a few hook methods in a fixed order. The hooks are overridden by subclasses or supplied by injected implementations. The skeleton is never changed; only what each step does changes.

#### Pattern structure
1. **Abstract Class**: defines the template method (the algorithm's skeleton) and declares the hook steps that can be replaced.
2. **Concrete Class**: provides concrete implementations of the hook steps, replacing the default steps in the abstract class.

#### Code

```go
package main

import "fmt"

// ReportGenerator is the "abstract class" for report generation, carrying the algorithm's skeleton.
// Go has no inheritance, and method calls on embedded structs are statically dispatched, so an "overridden" method in a subtype is never called by the template method.
// That's why function fields carry the hook steps here, and each concrete report type injects its own implementation at construction time.
type ReportGenerator struct {
    fetch    func()
    process  func()
    output   func()
}

// GenerateReport is the template method - it defines the algorithm's skeleton
func (r *ReportGenerator) GenerateReport() {
    r.fetch()
    r.process()
    r.output()
}

// NewReportGenerator creates a report generator with the default steps
func NewReportGenerator(fetch, process, output func()) *ReportGenerator {
    return &ReportGenerator{fetch: fetch, process: process, output: output}
}

// Concrete class - sales report generation, injecting the sales report's concrete steps
func NewSalesReportGenerator() *ReportGenerator {
    return NewReportGenerator(
        func() { fmt.Println("获取销售数据") },
        func() { fmt.Println("处理销售数据") },
        func() { fmt.Println("输出销售报表") },
    )
}

// Concrete class - financial report generation, injecting the financial report's concrete steps
func NewFinancialReportGenerator() *ReportGenerator {
    return NewReportGenerator(
        func() { fmt.Println("获取财务数据") },
        func() { fmt.Println("处理财务数据") },
        func() { fmt.Println("输出财务报表") },
    )
}

func main() {
    // Create the sales report generator
    salesReport := NewSalesReportGenerator()
    salesReport.GenerateReport()

    // Create the financial report generator
    financialReport := NewFinancialReportGenerator()
    financialReport.GenerateReport()
}
```

Output:

```
获取销售数据
处理销售数据
输出销售报表
获取财务数据
处理财务数据
输出财务报表
```

#### Applicable scenarios
- When several subclasses share the same algorithm skeleton and only some steps need different implementations.
- When you want to define the algorithm's structure in a base class while allowing subclasses to provide the concrete implementations.
- When implementation code is duplicated and the same algorithm structure shows up repeatedly; the Template Method pattern can cut the duplication.

#### Implementation
1. Define a struct that contains the template method and function fields (or an interface) to carry the hook steps.
2. Provide a constructor for each concrete report type that injects its own hook implementations.
3. Client code creates the concrete report generators through the constructors and calls the shared template method to run the algorithm.

#### Pros and cons
**Pros**:
- Defining the algorithm's skeleton in the base class avoids code duplication and keeps the algorithm's structure clear.
- Subclasses can selectively override individual steps to produce different variants.
- Easy to extend: adding a new step or changing an existing one does not affect the subclasses that already exist.

**Cons**:
- Can lead to tight coupling between the base class and the subclasses, since subclasses depend on the base class's template method.
- If the template method contains complex logic, the base class can become too large and complicated.

#### Relationship to other patterns
- **Template Method Pattern and Strategy Pattern**: the Strategy pattern defines a family of interchangeable algorithms, while the Template Method pattern defines the algorithm's skeleton in a base class and defers some steps to subclasses. They can be combined, for example using the Strategy pattern inside a template method to handle a concrete step.
- **Template Method Pattern and Factory Method Pattern**: the Factory Method pattern creates objects, while the Template Method pattern defines the algorithm's skeleton. They can be combined, for example using the Factory Method pattern inside a template method to create different objects.
- **Template Method Pattern and State Pattern**: the State pattern changes an object's behavior according to its state, while the Template Method pattern defines the algorithm's skeleton in a base class. They can be combined, for example using the State pattern inside a template method to manage the algorithm's steps.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Structural](/dp/Structural.md)
- [Visitor](/dp/Visitor.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Structural](/dp/Structural.md)
- [Visitor](/dp/Visitor.md)
