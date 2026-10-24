### Observer Pattern

#### Intent
The Observer pattern is a behavioral design pattern: when one object's state changes, the objects subscribed to it each receive a notification in turn and update accordingly. This is the prototype of the event publish-subscribe mechanism; the publisher does not need to know who the subscribers are.

#### Problem
Take news publishing. A newspaper publishes a story and all its subscribers need to receive it. If the newspaper's code hard-codes the notification logic one by one, then adding a channel means going back and changing the newspaper's side. The Observer pattern abstracts "the people being notified" into observers, and the publisher only broadcasts to the roster.

#### Solution
Define a Subject interface with methods to add and remove observers and to broadcast notifications; then define an Observer interface with a single update method. The Subject holds the list of observers, and when its state changes it walks the list and calls each one; each observer responds to the change in its update method.

#### Pattern structure
1. **Subject interface**: declares methods for adding and removing observers, as well as a method to notify observers.
2. **Concrete Subject**: implements the Subject interface, maintains the list of observers, and notifies them when its state changes.
3. **Observer interface**: declares an update method for responding to changes in the Subject's state.
4. **Concrete Observer**: implements the Observer interface and defines the concrete response operation when the Subject's state changes.

#### Code
Here is a Go implementation:

```go
package main

import "fmt"

// Observer interface
type Observer interface {
    Update(subject Subject)
}

// Subject interface
type Subject interface {
    AddObserver(observer Observer)
    RemoveObserver(observer Observer)
    NotifyObservers()
}

// Concrete Subject - price updater
type PriceUpdater struct {
    observers []Observer
    price     float64
}

func (p *PriceUpdater) AddObserver(observer Observer) {
    p.observers = append(p.observers, observer)
}

func (p *PriceUpdater) RemoveObserver(observer Observer) {
    for i, o := range p.observers {
        if o == observer {
            p.observers = append(p.observers[:i], p.observers[i+1:]...)
            break
        }
    }
}

func (p *PriceUpdater) NotifyObservers() {
    for _, observer := range p.observers {
        observer.Update(p)
    }
}

func (p *PriceUpdater) SetPrice(price float64) {
    p.price = price
    p.NotifyObservers()
}

func (p *PriceUpdater) GetPrice() float64 {
    return p.price
}

// Concrete Observer - consumer
type Consumer struct {
    name string
}

func (c *Consumer) Update(subject Subject) {
    if priceUpdater, ok := subject.(*PriceUpdater); ok {
        fmt.Printf("%s 收到价格更新: %.2f\n", c.name, priceUpdater.GetPrice())
    }
}

func main() {
    // create the price updater
    priceUpdater := &PriceUpdater{}

    // create the consumers
    consumer1 := &Consumer{name: "Alice"}
    consumer2 := &Consumer{name: "Bob"}

    // register the consumers with the price updater
    priceUpdater.AddObserver(consumer1)
    priceUpdater.AddObserver(consumer2)

    // update the price
    priceUpdater.SetPrice(99.99)
    priceUpdater.SetPrice(89.99)
}
```

#### Applicable scenarios
- You need to automatically notify multiple objects when one object's state changes, for example in an event-driven system.
- You need to reduce coupling between objects, making the system easier to extend and maintain.
- You need to implement a publish-subscribe mechanism, for example in a message-passing system or a real-time data update system.

#### Implementation
Define an interface at each end of the notification: the Subject interface handles registration and broadcasting, the Observer interface handles the response. The Concrete Subject maintains the observer list; each Concrete Observer writes its own reaction. Client code registers observers with the Subject, then just changes the state; the Subject does the broadcasting.

#### Pros and cons
**Pros**:
- Publishers and subscribers do not know each other; swapping either one does not require changing the other.
- Observers can be added and removed dynamically at runtime, so the notification roster changes with the business.
- Fits naturally into event-driven and real-time push scenarios.

**Cons**:
- With many observers, one notification is one traversal, so notification itself has overhead.
- If observers depend on each other, a jumbled notification order becomes hard to debug and system complexity goes up.

#### Relationship to other patterns
- **Observer Pattern and Mediator Pattern**: Mediator coordinates interactions between objects, while Observer handles notification after a state change; using Observers inside a Mediator to dispatch notifications lets the two be layered together.
- **Observer Pattern and Strategy Pattern**: Strategy handles swappable algorithms, while Observer handles broadcasting state changes; when a Strategy changes and its consumers need to be notified, you can send it out with Observers.
- **Observer Pattern and the event-driven model**: the Observer pattern is one way to implement an event-driven model; event publishing and subscribing land on it.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [ObjectPool](/dp/ObjectPool.md)
- [Proactor](/dp/Proactor.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ObjectPool](/dp/ObjectPool.md)
- [Proactor](/dp/Proactor.md)
