### 装饰器模式 (Decorator Pattern)

#### 意图
装饰器模式是结构型设计模式：把对象包进装饰器类，在不改原有类的前提下动态加职责。

#### 问题
在现实世界中，考虑一个简单的文本编辑器。最基本的功能是显示文本，但有时需要为文本添加不同的效果，例如加粗、斜体或下划线。如果直接在文本类中添加这些功能，会导致类的复杂度增加，且不易维护和扩展。

#### 解决方案
做法是为每种效果各写一个装饰器类，再按需要把它们层层包在文本对象外面。

#### 模式结构
1. **组件（Component）**：定义了将要动态添加职责的对象接口。
2. **具体组件（Concrete Component）**：实现了组件接口，是将要被装饰的对象。
3. **装饰器（Decorator）**：实现了组件接口，持有一个组件对象，并在其基础上扩展功能。
4. **具体装饰器（Concrete Decorator）**：继承装饰器，并实现具体的装饰功能。

#### 代码
装饰器模式的 Go 实现：

```go
package main

import "fmt"

// 组件接口
type Component interface {
    Operation() string
}

// 具体组件 - 文本
type Text struct {
    content string
}

func (t *Text) Operation() string {
    return t.content
}

// 装饰器基类
type Decorator struct {
    component Component
}

func (d *Decorator) Operation() string {
    if d.component != nil {
        return d.component.Operation()
    }
    return ""
}

// 具体装饰器 - 加粗
type BoldDecorator struct {
    Decorator
}

func (b *BoldDecorator) Operation() string {
    return "<b>" + b.Decorator.Operation() + "</b>"
}

// 具体装饰器 - 斜体
type ItalicDecorator struct {
    Decorator
}

func (i *ItalicDecorator) Operation() string {
    return "<i>" + i.Decorator.Operation() + "</i>"
}

// 具体装饰器 - 下划线
type UnderlineDecorator struct {
    Decorator
}

func (u *UnderlineDecorator) Operation() string {
    return "<u>" + u.Decorator.Operation() + "</u>"
}

func main() {
    text := &Text{content: "Hello, World!"}

    boldText := &BoldDecorator{Decorator{component: text}}
    italicBoldText := &ItalicDecorator{Decorator{component: boldText}}
    underlinedItalicBoldText := &UnderlineDecorator{Decorator{component: italicBoldText}}

    fmt.Println("原始文本:", text.Operation())
    fmt.Println("加粗文本:", boldText.Operation())
    fmt.Println("加粗斜体文本:", italicBoldText.Operation())
    fmt.Println("加粗斜体下划线文本:", underlinedItalicBoldText.Operation())
}
```

#### 适用场景
- 需要在不改变原有类的情况下，动态地为对象添加职责时。
- 需要为一组对象添加相同的职责，且职责可以动态组合时。

#### 实现方式
1. 定义组件接口，声明将要动态添加职责的对象接口。
2. 创建具体组件，实现组件接口。
3. 创建装饰器基类，实现组件接口，并持有一个组件对象。
4. 创建具体装饰器，继承装饰器基类，并实现具体的装饰功能。
5. 在客户端代码中，通过装饰器类动态地为组件对象添加职责。

#### 优缺点
**优点**：
- 动态地为对象添加新职责，而不影响其他对象。
- 可以通过多个装饰器组合，形成复杂的功能。
- 符合开闭原则，可以通过添加新的装饰器类来扩展系统，而不会影响现有代码。

**缺点**：
- 可能会导致大量的小类，增加系统的复杂度。
- 多个装饰器的组合可能会导致调试困难。

#### 其他模式的关系
- **代理模式（Proxy Pattern）**：结构和装饰器类似，代理控制访问，装饰器加职责。
- **适配器模式（Adapter Pattern）**：适配器把一个接口换成另一个，装饰器不换接口，只加职责。
- **组合模式（Composite Pattern）**：组合把对象拼成树形结构表示“部分-整体”，装饰器是在单个对象外面层层包裹。