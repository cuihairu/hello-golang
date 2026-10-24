### Command Pattern

#### Intent
The Command pattern is a behavioral design pattern: wrap a request in an object, so the sender just hands it off and doesn't care who executes it or how. Once a request is an object, you can queue it, log it, and undo and redo it.

#### Problem
Take using a remote control for devices like a TV or a light bulb. If every device's operations are written directly into the remote, adding one device means changing the remote's code. The Command pattern wraps each operation in its own command object; the remote only knows about commands, never about the concrete devices.

#### Solution
First define a command interface that declares the method for executing an operation. Concrete commands implement that interface, bundling the operation logic together with the receiver they control. The remote holds command objects and calls their execute method when a button is pressed. Sender and executor are now decoupled; adding a new operation only takes one more command class, and the remote stays untouched.

#### Pattern structure
1. **Command interface (Command)**: declares the method for executing an operation.
2. **Concrete Command**: implements the command interface, encapsulating the request's operation and its receiver object.
3. **Receiver**: the object that actually performs the operation.
4. **Invoker**: calls the command object to execute the request.
5. **Client**: creates the concrete command objects and wires up the receiver and invoker.

#### Code
Here's a Go implementation:

```go
package main

import "fmt"

// Command interface
type Command interface {
    Execute()
}

// Receiver - TV
type TV struct{}

func (t *TV) TurnOn() {
    fmt.Println("电视已开启")
}

func (t *TV) TurnOff() {
    fmt.Println("电视已关闭")
}

// Concrete command - turn on the TV
type TurnOnCommand struct {
    tv *TV
}

func (c *TurnOnCommand) Execute() {
    c.tv.TurnOn()
}

// Concrete command - turn off the TV
type TurnOffCommand struct {
    tv *TV
}

func (c *TurnOffCommand) Execute() {
    c.tv.TurnOff()
}

// Invoker - remote control
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

    // create the commands
    turnOn := &TurnOnCommand{tv: tv}
    turnOff := &TurnOffCommand{tv: tv}

    // create the remote control
    remote := &RemoteControl{}

    // use the remote to turn the TV on
    remote.SetCommand(turnOn)
    remote.PressButton()

    // use the remote to turn the TV off
    remote.SetCommand(turnOff)
    remote.PressButton()
}
```

#### Use cases
- When you need to decouple the sender of a request from its handler.
- When you need to support undo and redo of operations.
- When you need to queue requests or log them.
- When you need to configure a request's parameters dynamically.

#### Implementation
The client first builds the receiver, then attaches a concrete command object to it and hands it to the invoker for safekeeping. After that the invoker just triggers the command without needing to know which device or action is wrapped inside. Adding a new operation only means adding one concrete command class.

#### Pros and cons
**Pros**:
- The sender doesn't know who the receiver is, so swapping in a different execution path doesn't require changing the sender.
- Once a request is an object, undo, redo, queueing, and logging all become easy.
- Queueing, logging, and transaction handling, none of it tied to the request itself, can be written separately from the concrete execution.

**Cons**:
- One command class per operation, so the class count climbs as operations grow, and the codebase balloons with it.

#### Relations to other patterns
- **Command Pattern and Chain of Responsibility Pattern**: the Chain of Responsibility pattern passes a request down a chain of handlers, while the Command pattern wraps the request in an object; hand a command object to the chain and each link in it can process it in turn.
- **Command Pattern and Strategy Pattern**: Strategy decides which algorithm to use, Command decides which action to perform, and the two can nest — a command object can hold a strategy to pick the concrete action.
- **Command Pattern and Template Method Pattern**: Template Method sets the algorithm skeleton and lets subclasses fill in the steps, while Command just wraps the call; you can use a template method inside the command object to fix the steps of the operation.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [ChainofResponsibility](/dp/ChainofResponsibility.md)
- [Composite](/dp/Composite.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ChainofResponsibility](/dp/ChainofResponsibility.md)
- [Composite](/dp/Composite.md)
