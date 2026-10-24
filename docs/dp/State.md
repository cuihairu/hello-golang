### State Pattern

#### Intent
The State pattern is a behavioral design pattern that lets an object change its behavior when its internal state changes. By moving state-specific behavior into separate state objects, the State pattern makes an object's state changes look, from the outside, like changes in its behavior, which simplifies state management and state-switching logic.

#### Problem
Take a network connection object: it has states such as connecting, connected, disconnected, and connection failed, and the same request behaves differently in each state. Cram all of that state logic into one class and the class grows bloated, making it hard to extend and maintain. Splitting the behavior of each state into independent state objects keeps state management light.

#### Solution
Use the State pattern: define a state interface that declares each state's behavior, then write a concrete state class for every state. The context object holds a reference to the current state and delegates state-related behavior to it; swap in a different state object and the context's behavior changes with it.

#### Pattern structure
1. **State interface**: defines the state-specific behavior interface.
2. **Concrete State**: implements the state interface and defines the concrete state behavior.
3. **Context**: holds a reference to the current state and delegates state-related behavior to the current state object. The context object can change its state object at runtime.

#### Code

```go
package main

import "fmt"

// State interface
type State interface {
    HandleRequest(context *Context)
}

// Concrete state - connected
type ConnectedState struct{}

func (s *ConnectedState) HandleRequest(context *Context) {
    fmt.Println("处理已连接状态下的请求")
    context.SetState(&DisconnectedState{})
}

// Concrete state - disconnected
type DisconnectedState struct{}

func (s *DisconnectedState) HandleRequest(context *Context) {
    fmt.Println("处理断开连接的请求")
    context.SetState(&ConnectingState{})
}

// Concrete state - connecting
type ConnectingState struct{}

func (s *ConnectingState) HandleRequest(context *Context) {
    fmt.Println("处理连接中的请求")
    context.SetState(&ConnectedState{})
}

// Context - network connection
type Context struct {
    state State
}

func (c *Context) SetState(state State) {
    c.state = state
}

func (c *Context) Request() {
    c.state.HandleRequest(c)
}

func main() {
    // Create the context object
    context := &Context{}

    // Set the initial state
    context.SetState(&ConnectingState{})

    // Handle requests; the state changes along the way
    context.Request()
    context.Request()
    context.Request()
    context.Request()
}
```

#### Applicable scenarios
- When an object's behavior depends on its state and the state changes frequently.
- When the state logic is complex and needs to change dynamically according to state.
- When you want to simplify the code and make the system more extensible by separating the state logic, for example when implementing a state machine or a workflow management system.

#### Implementation
1. Define a state interface that declares the state-specific behavior methods.
2. Create concrete state classes that implement the state interface and define the concrete behavior logic.
3. Define a context class that holds a reference to the current state and delegates state-related behavior to the current state object.
4. Client code creates the context object and the concrete state objects, and manages state switching and behavior execution through the context object.

#### Pros and cons
**Pros**:
- The State pattern moves state-related behavior into separate state objects, which reduces the number of conditional statements and makes state management clearer and more maintainable.
- By switching state objects you can change the context object's behavior dynamically, which suits scenarios where state changes often.
- Adding a new state becomes easy: just add a new state class, with no need to modify existing code.

**Cons**:
- It may introduce a large number of state classes, increasing system complexity.
- Switching between states can become complicated, especially when the state logic is complex.

#### Relationship to other patterns
- **State Pattern and Strategy Pattern**: the Strategy pattern defines a family of interchangeable algorithms, while the State pattern changes an object's behavior according to its state. The two can be combined, for example using the Strategy pattern inside the State pattern to define the behavior of each state.
- **State Pattern and Chain of Responsibility Pattern**: the Chain of Responsibility pattern passes requests along a processing chain, while the State pattern manages an object's state and changes its behavior. They can be combined, for example using the Chain of Responsibility pattern inside the State pattern to handle requests within a state.
- **State Pattern and Command Pattern**: the Command pattern wraps the operations of a request, while the State pattern manages an object's state. They can be combined, for example using the Command pattern inside the State pattern to execute operations in a state.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Singleton](/dp/Singleton.md)
- [Strategy](/dp/Strategy.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Singleton](/dp/Singleton.md)
- [Strategy](/dp/Strategy.md)
