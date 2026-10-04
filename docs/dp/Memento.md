### 备忘录模式 (Memento Pattern)

#### 意图
备忘录模式是一种行为型设计模式：把对象的状态存进一个单独的对象，需要时再取回来恢复，对外不暴露内部状态。它通常用于实现撤销和重做。

#### 问题
在现实世界中，考虑一个文本编辑器，用户可能会在编辑过程中需要撤销或重做某些操作。如果每次都直接修改对象状态，可能会使得撤销和恢复操作变得复杂。备忘录模式可以通过保存和恢复对象状态来简化这些操作。

#### 解决方案
使用备忘录模式，我们可以定义一个备忘录类来保存对象的状态，并定义一个发起人类来创建和恢复备忘录。发起人类包含要保存和恢复的状态，而备忘录类只负责保存这些状态，不允许直接修改。一个管理者类（如备忘录管理器）用于存储和管理备忘录实例。

#### 模式结构
1. **发起人（Originator）**：负责创建一个备忘录对象，用于保存当前的状态，以及使用备忘录对象恢复状态。
2. **备忘录（Memento）**：保存发起人对象的内部状态。备忘录类只能被发起人访问，不允许直接修改。
3. **管理者（Caretaker）**：负责保存和恢复备忘录对象，但不允许访问备忘录的内部状态。

#### 代码

```go
package main

import "fmt"

// 发起人 - 文本编辑器
type Editor struct {
    text string
}

func (e *Editor) SetText(text string) {
    e.text = text
}

func (e *Editor) CreateMemento() *Memento {
    return &Memento{state: e.text}
}

func (e *Editor) Restore(memento *Memento) {
    e.text = memento.state
}

func (e *Editor) GetText() string {
    return e.text
}

// 备忘录 - 保存状态
type Memento struct {
    state string
}

// 管理者 - 备忘录管理器
type Caretaker struct {
    mementos []*Memento
}

func (c *Caretaker) AddMemento(memento *Memento) {
    c.mementos = append(c.mementos, memento)
}

func (c *Caretaker) GetMemento(index int) *Memento {
    if index >= 0 && index < len(c.mementos) {
        return c.mementos[index]
    }
    return nil
}

func main() {
    editor := &Editor{}
    caretaker := &Caretaker{}

    // 设置文本
    editor.SetText("版本 1")
    caretaker.AddMemento(editor.CreateMemento())

    editor.SetText("版本 2")
    caretaker.AddMemento(editor.CreateMemento())

    editor.SetText("版本 3")
    caretaker.AddMemento(editor.CreateMemento())

    // 恢复到版本 1
    editor.Restore(caretaker.GetMemento(0))
    fmt.Println("恢复后的文本:", editor.GetText())

    // 恢复到版本 2
    editor.Restore(caretaker.GetMemento(1))
    fmt.Println("恢复后的文本:", editor.GetText())
}
```

#### 适用场景
- 需要实现撤销和重做，例如文本编辑器、图形编辑器。
- 需要保存历史状态并在任意时刻恢复，同时不暴露对象的内部状态。

#### 实现方式
1. 定义发起人类，包含要保存的状态，并提供创建和恢复备忘录的方法。
2. 定义备忘录类，保存发起人对象的内部状态，并只允许发起人访问。
3. 定义管理者类，负责保存和恢复备忘录对象，并提供获取备忘录的方法。
4. 客户端代码创建发起人对象、备忘录对象和管理者对象，并执行保存和恢复操作。

#### 优缺点
**优点**：
- 可以实现撤销和恢复功能，使得对象状态管理更加灵活。
- 不暴露对象内部状态，从而保护对象的封装性。
- 允许保存对象的多个状态，并根据需要恢复到任意状态。

**缺点**：
- 对象状态很大时，备忘录会占用大量内存，数量一多更明显。
- 备忘录的存储和生命周期要自己管理，会增加一部分复杂性。

#### 其他模式的关系
- **备忘录模式与命令模式（Command Pattern）**：命令封装请求的操作，备忘录保存状态；命令模式借备忘录实现撤销和重做。
- **备忘录模式与状态模式（State Pattern）**：状态模式按当前状态切换行为，备忘录用来保存状态的历史记录。
- **备忘录模式与观察者模式（Observer Pattern）**：观察者模式在状态变化时通知观察者，备忘录负责存下可恢复的那份状态，两者可以配合实现撤销。