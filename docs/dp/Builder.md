### 生成器模式 (Builder Pattern)

#### 意图
生成器模式是一种创建型设计模式，它通过一步一步构建复杂对象的方式，使得同样的构建过程可以创建不同的表示。生成器模式将一个复杂对象的构建与其表示分离，使得同样的构建过程可以创建不同的表示。

#### 问题
在现实世界中，考虑一个复杂的文档生成系统，该系统需要生成不同格式的文档（例如HTML、PDF、Markdown）。每种文档格式都有不同的生成过程。如果在主应用中硬编码这些生成过程，会导致代码难以维护和扩展。

#### 解决方案
使用生成器模式，我们可以定义一个文档生成器接口和多个具体的文档生成器实现类，通过生成器逐步构建文档对象，从而使得客户端代码与具体的文档生成过程无关。

#### 模式结构
1. **生成器接口（Builder）**：定义创建复杂对象各个部分的方法。
2. **具体生成器（ConcreteBuilder）**：实现生成器接口，提供创建复杂对象各个部分的具体实现。
3. **产品（Product）**：表示生成的复杂对象。
4. **指挥者（Director）**：负责调用生成器对象中的方法以创建复杂对象。

#### 代码
以下是使用Go语言实现的生成器模式示例：

```go
package main

import "fmt"

// 文档表示产品
type Document struct {
    Content string
}

// 文档生成器接口
type DocumentBuilder interface {
    SetTitle(title string)
    SetBody(body string)
    SetFooter(footer string)
    GetDocument() *Document
}

// HTML 文档生成器
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

// Markdown 文档生成器
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

// 指挥者
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
    // 构建 HTML 文档
    htmlBuilder := NewHTMLBuilder()
    director := NewDirector(htmlBuilder)
    director.Construct("HTML Title", "This is the body of the HTML document.", "HTML Footer")
    htmlDocument := htmlBuilder.GetDocument()
    fmt.Println("HTML Document:")
    fmt.Println(htmlDocument.Content)

    // 构建 Markdown 文档
    markdownBuilder := NewMarkdownBuilder()
    director = NewDirector(markdownBuilder)
    director.Construct("Markdown Title", "This is the body of the Markdown document.", "Markdown Footer")
    markdownDocument := markdownBuilder.GetDocument()
    fmt.Println("Markdown Document:")
    fmt.Println(markdownDocument.Content)
}
```

#### 适用场景
- 需要创建复杂对象时，该对象由多个部分组成，并且需要一步一步构建。
- 同样的构建过程需要生成不同的表示时。
- 需要控制复杂对象的构建过程时。

#### 实现方式
1. 创建生成器接口，定义创建复杂对象各个部分的方法。
2. 创建具体生成器类，实现生成器接口，提供创建复杂对象各个部分的具体实现。
3. 创建产品类，表示生成的复杂对象。
4. 创建指挥者类，负责调用生成器对象中的方法以创建复杂对象。

#### 优缺点
**优点**：
- 使客户端不必知道产品内部组成的细节。
- 各个具体生成器相互独立，有利于系统的扩展。
- 可以更精细地控制产品的创建过程。

**缺点**：
- 增加了系统的复杂性，需要定义多个具体生成器类。

#### 其他模式的关系
- **抽象工厂模式（Abstract Factory Pattern）**：生成器模式与抽象工厂模式的目的类似，都是创建复杂对象。不同之处在于，生成器模式更加关注一步一步创建对象的过程，而抽象工厂模式侧重于创建一系列相关对象。
- **工厂方法模式（Factory Method Pattern）**：工厂方法模式通常与生成器模式结合使用，以便于创建复杂对象的部分组件。