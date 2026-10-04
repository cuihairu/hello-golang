### 命令模式 (Command Pattern)

#### 意图
命令模式是一种行为型设计模式：把请求封装成对象，发送请求的一方只管交出去，不关心谁执行、怎么执行。请求变成对象之后，就能排队、记日志，也能撤销和重做。

#### 问题
拿遥控器控制电视、灯泡这类设备来说，如果每台设备的操作都直接写在遥控器里，加一台设备就得改遥控器代码。命令模式把每个操作封装成独立的命令对象，遥控器只认识命令，不认识具体设备。

#### 解决方案
先定义一个命令接口，声明执行操作的方法；具体命令实现这个接口，把操作逻辑和它要控制的接收者一起封在对象里。遥控器持有命令对象，按下按钮时调用它的执行方法。调用方和执行方就此分开，加新操作只需新增一个命令类，遥控器不用动。

#### 模式结构
1. **命令接口（Command）**：声明执行操作的方法。
2. **具体命令（Concrete Command）**：实现命令接口，封装请求的操作和接收者对象。
3. **接收者（Receiver）**：实际执行操作的对象。
4. **调用者（Invoker）**：调用命令对象执行请求。
5. **客户端（Client）**：创建具体命令对象，并设置接收者和调用者。

#### 代码
用 Go 实现一遍：

```go
package main

import "fmt"

// 命令接口
type Command interface {
    Execute()
}

// 接收者 - 电视
type TV struct{}

func (t *TV) TurnOn() {
    fmt.Println("电视已开启")
}

func (t *TV) TurnOff() {
    fmt.Println("电视已关闭")
}

// 具体命令 - 打开电视命令
type TurnOnCommand struct {
    tv *TV
}

func (c *TurnOnCommand) Execute() {
    c.tv.TurnOn()
}

// 具体命令 - 关闭电视命令
type TurnOffCommand struct {
    tv *TV
}

func (c *TurnOffCommand) Execute() {
    c.tv.TurnOff()
}

// 调用者 - 遥控器
type RemoteControl struct {
    command Command
}

func (r *RemoteControl) SetCommand(command Command) {
    r.command = command
}

func (r *RemoteControl) PressButton() {
    r.command.Execute()
}

func main() {
    tv := &TV{}

    // 创建命令
    turnOn := &TurnOnCommand{tv: tv}
    turnOff := &TurnOffCommand{tv: tv}

    // 创建遥控器
    remote := &RemoteControl{}

    // 使用遥控器打开电视
    remote.SetCommand(turnOn)
    remote.PressButton()

    // 使用遥控器关闭电视
    remote.SetCommand(turnOff)
    remote.PressButton()
}
```

#### 适用场景
- 需要将请求的发起者与处理者解耦时。
- 需要支持操作的撤销和重做时。
- 需要将请求排队或记录日志时。
- 需要支持动态地配置请求的参数时。

#### 实现方式
客户端先造好接收者，再给它配上具体的命令对象，交给调用者保管。之后调用者只管触发命令，不必知道命令里裹的是哪台设备、哪个动作。要加一种新操作，只需补一个具体命令类。

#### 优缺点
**优点**：
- 发起方不知道接收方是谁，换一套执行逻辑不用改发起方。
- 请求成了对象，撤销、重做、排队、记日志都好做。
- 与请求本身无关的排队、日志、事务处理，可以和具体执行分开写。

**缺点**：
- 一个操作对应一个命令类，操作多了类的数量就上来了，代码量先涨一块。

#### 其他模式的关系
- **命令模式与责任链模式（Chain of Responsibility Pattern）**：责任链把请求沿处理链往下传，命令则把请求封成对象；把命令对象交给责任链，链上各环节就能逐个处理它。
- **命令模式与策略模式（Strategy Pattern）**：策略管选哪个算法，命令管执行哪个动作，两者能嵌套：命令对象里持一个策略来决定具体动作。
- **命令模式与模板方法模式（Template Method Pattern）**：模板方法定算法骨架、由子类填步骤，命令只管封装调用，可以在命令对象里用模板方法固定操作的步骤。