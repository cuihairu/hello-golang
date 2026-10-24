### Builder Pattern

#### Intent
The Builder pattern is a creational design pattern: it breaks the construction of a complex object into step-by-step stages. The construction process itself is reusable, and the product is a different representation.

#### Problem
In the real world, consider a complex document generation system that needs to produce documents in different formats (such as HTML, PDF, and Markdown). Each document format has a different generation process. If these generation processes are hardcoded into the main application, the code becomes hard to maintain and extend.

#### Solution
Use the Builder pattern: define a document builder interface and several concrete document builder classes. Build the document object step by step through the builder, so the client code stays independent of the concrete document generation process.

#### Structure
1. **Builder**: defines the methods for creating the parts of the complex object.
2. **ConcreteBuilder**: implements the builder interface and provides the concrete implementation for creating the parts of the complex object.
3. **Product**: represents the complex object being produced.
4. **Director**: calls the methods on the builder object to assemble the complex object.

#### Code

```go
package main

import "fmt"

// Document represents the product
type Document struct {
    Content string
}

// Document builder interface
type DocumentBuilder interface {
    SetTitle(title string)
    SetBody(body string)
    SetFooter(footer string)
    GetDocument() *Document
}

// HTML document builder
type HTMLBuilder struct {
    document *Document
}

func NewHTMLBuilder() *HTMLBuilder {
    return &HTMLBuilder{&Document{}}
}

func (b *HTMLBuilder) SetTitle(title string) {
    b.document.Content += fmt.Sprintf("<h1>%s</h1>\n", title)
}

func (b *HTMLBuilder) SetBody(body string) {
    b.document.Content += fmt.Sprintf("<p>%s</p>\n", body)
}

func (b *HTMLBuilder) SetFooter(footer string) {
    b.document.Content += fmt.Sprintf("<footer>%s</footer>\n", footer)
}

func (b *HTMLBuilder) GetDocument() *Document {
    return b.document
}

// Markdown document builder
type MarkdownBuilder struct {
    document *Document
}

func NewMarkdownBuilder() *MarkdownBuilder {
    return &MarkdownBuilder{&Document{}}
}

func (b *MarkdownBuilder) SetTitle(title string) {
    b.document.Content += fmt.Sprintf("# %s\n\n", title)
}

func (b *MarkdownBuilder) SetBody(body string) {
    b.document.Content += fmt.Sprintf("%s\n\n", body)
}

func (b *MarkdownBuilder) SetFooter(footer string) {
    b.document.Content += fmt.Sprintf("---\n%s\n", footer)
}

func (b *MarkdownBuilder) GetDocument() *Document {
    return b.document
}

// Director
type Director struct {
    builder DocumentBuilder
}

func NewDirector(builder DocumentBuilder) *Director {
    return &Director{builder}
}

func (d *Director) Construct(title, body, footer string) {
    d.builder.SetTitle(title)
    d.builder.SetBody(body)
    d.builder.SetFooter(footer)
}

func main() {
    // build an HTML document
    htmlBuilder := NewHTMLBuilder()
    director := NewDirector(htmlBuilder)
    director.Construct("HTML Title", "This is the body of the HTML document.", "HTML Footer")
    htmlDocument := htmlBuilder.GetDocument()
    fmt.Println("HTML Document:")
    fmt.Println(htmlDocument.Content)

    // build a Markdown document
    markdownBuilder := NewMarkdownBuilder()
    director = NewDirector(markdownBuilder)
    director.Construct("Markdown Title", "This is the body of the Markdown document.", "Markdown Footer")
    markdownDocument := markdownBuilder.GetDocument()
    fmt.Println("Markdown Document:")
    fmt.Println(markdownDocument.Content)
}
```

#### Use cases
- You need to create a complex object composed of multiple parts that must be built step by step.
- The same construction process needs to produce different representations.
- You need to control the construction process of the complex object.

#### Implementation
Start with a builder interface (such as `DocumentBuilder`), then write one concrete builder per output format (`HTMLBuilder`, `MarkdownBuilder`); the product is the final `Document`; the director `Director` calls `SetTitle`/`SetBody`/`SetFooter` in a fixed order, and the client only talks to the director.

#### Pros and cons
**Pros**:
- The client no longer needs to know the details of how the product is put together.
- The concrete builders are independent of each other, which helps the system extend.
- The product creation process can be controlled more precisely.

**Cons**:
- Adds complexity to the system because multiple concrete builder classes must be defined.

#### Relationship to other patterns
- **Abstract Factory Pattern**: the Builder pattern and the Abstract Factory pattern serve similar purposes — both create complex objects. The difference is that the Builder pattern focuses on the step-by-step process of creating an object, while the Abstract Factory pattern focuses on creating a family of related objects.
- **Factory Method Pattern**: the Factory Method pattern is usually combined with the Builder pattern to make it easier to create individual parts of a complex object.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Bridge](/dp/Bridge.md)
- [ChainofResponsibility](/dp/ChainofResponsibility.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ChainofResponsibility](/dp/ChainofResponsibility.md)
