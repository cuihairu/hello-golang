### 组合模式 (Composite Pattern)

#### 意图
组合模式是一种结构型设计模式，它把对象组合成树形结构来表示“部分-整体”的层次，客户端因此不用区分单个对象和组合对象，同一套调用都适用。

#### 问题
在现实世界中，考虑一个图形编辑器的场景。一个图形可以是一个简单的形状（例如线条、圆形、矩形），也可以是由多个简单形状组成的复杂图形。如果没有组合模式，客户端代码需要分别处理简单形状和复杂图形，增加了代码的复杂性。

#### 解决方案
组合模式的做法是定一个统一的接口，简单形状和复杂图形都实现它，客户端只面向这个接口调用。

#### 模式结构
1. **组件（Component）**：定义了组合对象和叶子对象的统一接口。
2. **叶子（Leaf）**：表示组合中的基本元素，不包含其他子对象。
3. **组合（Composite）**：包含子组件，表示一个可以包含其他叶子或组合的对象。
4. **客户端（Client）**：通过组件接口与组合结构中的对象交互。

#### 代码
以下是使用Go语言实现的组合模式示例：

```go
package main

import "fmt"

// 组件接口
type Graphic interface {
    Draw()
}

// 叶子 - 圆形
type Circle struct{}

func (c *Circle) Draw() {
    fmt.Println("绘制一个圆形")
}

// 叶子 - 矩形
type Rectangle struct{}

func (r *Rectangle) Draw() {
    fmt.Println("绘制一个矩形")
}

// 组合 - 复杂图形
type CompositeGraphic struct {
    graphics []Graphic
}

func (cg *CompositeGraphic) Add(graphic Graphic) {
    cg.graphics = append(cg.graphics, graphic)
}

func (cg *CompositeGraphic) Remove(graphic Graphic) {
    for i, g := range cg.graphics {
        if g == graphic {
            cg.graphics = append(cg.graphics[:i], cg.graphics[i+1:]...)
            break
        }
    }
}

func (cg *CompositeGraphic) Draw() {
    for _, graphic := range cg.graphics {
        graphic.Draw()
    }
}

func main() {
    circle1 := &Circle{}
    circle2 := &Circle{}
    rectangle := &Rectangle{}

    // 创建一个组合图形，并添加基本图形
    composite := &CompositeGraphic{}
    composite.Add(circle1)
    composite.Add(circle2)
    composite.Add(rectangle)

    // 绘制组合图形
    fmt.Println("绘制组合图形:")
    composite.Draw()

    // 移除一个基本图形，再次绘制组合图形
    composite.Remove(circle1)
    fmt.Println("移除一个圆形后，绘制组合图形:")
    composite.Draw()
}
```

#### 适用场景
- 需要表示对象的部分-整体层次结构时。
- 希望客户端能够一致地处理单个对象和组合对象时。

#### 实现方式
实现分四步：先定组件接口，声明统一操作；再写实现该接口的叶子类；然后写组合类，持有一组子组件并实现添加、移除方法；客户端全程只面向组件接口。

#### 优缺点
**优点**：
- 层次结构清晰，加新的叶子或组合对象不用改客户端。
- 单个对象和组合对象走同一套调用，客户端代码短一截。

**缺点**：
- 设计较为复杂，可能需要更多的类和接口。
- 如果过度使用组合模式，可能会导致系统层次结构过于复杂。

#### 其他模式的关系
- **装饰器模式（Decorator Pattern）**：装饰器动态地给单个对象加职责，组合模式组织的是对象树。
- **享元模式（Flyweight Pattern）**：享元靠共享对象省内存，和组合模式解决的问题不同。
- **迭代器模式（Iterator Pattern）**：组合模式可以与迭代器模式结合使用，以便遍历组合结构中的所有对象。