### Mediator Pattern

#### Intent
The Mediator pattern is a behavioral design pattern that encapsulates the interactions among a group of objects in a single mediator object: the objects no longer call each other, they all go to the mediator, so a web of dependencies collapses into a single center.

#### Problem
In the real world, consider a complex chat system where multiple users can send messages to each other. If every user communicates directly with the others, the system complexity gets very high and managing message passing becomes difficult. The Mediator pattern can introduce a chat mediator object to coordinate message passing between users, thereby simplifying the system design.

#### Solution
With the Mediator pattern, we can define a mediator interface that declares methods for coordinating interactions between objects. Then create concrete mediator classes that implement the interface and provide the logic for interactions between objects. Colleague objects communicate through the mediator rather than directly with each other.

#### Pattern structure
1. **Mediator interface**: declares methods for coordinating interactions between objects.
2. **Concrete Mediator**: implements the Mediator interface and provides the concrete logic for coordinating interactions between objects.
3. **Colleague**: defines the interface for interacting with the mediator, holds a reference to the mediator, and interacts through the mediator.
4. **Concrete Colleague**: implements the Colleague interface and performs concrete interactions through the mediator.

#### Code

```go
package main

import "fmt"

// Mediator interface
type Mediator interface {
    Send(message string, colleague Colleague)
}

// Colleague interface
type Colleague interface {
    Send(message string)
    Receive(message string)
}

// Concrete Mediator - chat mediator
type ChatMediator struct {
    colleagues map[string]Colleague
}

func (m *ChatMediator) Register(name string, colleague Colleague) {
    if m.colleagues == nil {
        m.colleagues = make(map[string]Colleague)
    }
    m.colleagues[name] = colleague
}

func (m *ChatMediator) Send(message string, colleague Colleague) {
    for _, c := range m.colleagues {
        if c != colleague {
            c.Receive(message)
        }
    }
}

// Concrete Colleague - user
type User struct {
    name     string
    mediator Mediator
}

func (u *User) Send(message string) {
    fmt.Printf("%s: 发送消息: %s\n", u.name, message)
    u.mediator.Send(message, u)
}

func (u *User) Receive(message string) {
    fmt.Printf("%s: 接收到消息: %s\n", u.name, message)
}

func main() {
    // create the mediator
    mediator := &ChatMediator{}

    // create the users
    user1 := &User{name: "Alice", mediator: mediator}
    user2 := &User{name: "Bob", mediator: mediator}
    user3 := &User{name: "Charlie", mediator: mediator}

    // register the users with the mediator
    mediator.Register("Alice", user1)
    mediator.Register("Bob", user2)
    mediator.Register("Charlie", user3)

    // users send messages
    user1.Send("你好，大家好!")
    user2.Send("嗨，Alice!")
    user3.Send("大家好!")
}
```

#### Applicable scenarios
- You need to handle complex interactions among multiple objects, and the interaction logic may become complex.
- You need to reduce direct dependencies between objects, to make the system easier to maintain and extend.
- You need to centrally manage the interaction logic between objects, for example in a chat system or an event-handling system.

#### Implementation
1. Define the Mediator interface, declaring methods for coordinating interactions between objects.
2. Create a concrete mediator class that implements the Mediator interface and provides the logic for interactions between objects.
3. Define the Colleague interface, declaring methods for interacting with the mediator, and holding a reference to the mediator.
4. Create concrete colleague classes that implement the Colleague interface and perform concrete interactions through the mediator.
5. Client code creates the mediator and colleague objects, sets the mediator on the colleague objects, and then begins interaction.

#### Pros and cons
**Pros**:
- Reduces direct coupling between objects, making the system more flexible to extend and maintain.
- Centrally manages the interaction logic between objects, simplifying system complexity.
- Interaction logic can be adjusted and changed dynamically without modifying the code of the participant objects.

**Cons**:
- The mediator object may become complex, because it has to handle all the interaction logic.
- The Mediator pattern may introduce additional classes, increasing system complexity.

#### Relationship to other patterns
- **Mediator Pattern and Observer Pattern**: Observer notifies observers when an object's state changes, while Mediator coordinates interactions between objects. Mediator can be used together with Observer, for example managing observer notifications inside the mediator.
- **Mediator Pattern and Chain of Responsibility Pattern**: Chain of Responsibility passes requests along a handling chain, while Mediator centrally coordinates interactions between objects. The two can be combined, for example implementing chain-of-responsibility logic inside the mediator.
- **Mediator Pattern and Command Pattern**: Command encapsulates operations as requests, while Mediator coordinates interactions between objects. They can be combined, for example using command objects inside the mediator to handle requests.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Iterator](/dp/Iterator.md)
- [Memento](/dp/Memento.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Iterator](/dp/Iterator.md)
- [Memento](/dp/Memento.md)
