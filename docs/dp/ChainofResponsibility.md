### Chain of Responsibility Pattern

#### Intent
The Chain of Responsibility pattern is a behavioral design pattern: a request is passed along a chain of handler objects, and each object in the chain has a chance to handle it. The sender does not know which one ends up handling it, which decouples the two sides.

#### Problem
Take a customer service system: requests come in several types — technical support, billing inquiries, and so on. If the sender has to decide who handles each request type, it has to know every handler, and both coupling and complexity go up. Let the request travel down the handler chain on its own, and the sender no longer needs to care about any of this.

#### Solution
String the handler objects together into a chain: each object handles the request types it recognizes and forwards the rest to the next one. Swapping handlers or reordering them does not require touching the sender's code.

#### Structure
1. **Handler**: defines the interface for handling requests, including a method to set the next handler.
2. **Concrete Handler**: implements the request-handling logic and passes the request along to the next handler in the chain.
3. **Client**: creates the handler chain and issues the requests.

#### Code
Go implementation:

```go
package main

import "fmt"

// Handler interface
type Handler interface {
    SetNext(handler Handler)
    HandleRequest(request string)
}

// Concrete handler - technical support handler
type TechSupportHandler struct {
    next Handler
}

func (t *TechSupportHandler) SetNext(handler Handler) {
    t.next = handler
}

func (t *TechSupportHandler) HandleRequest(request string) {
    if request == "技术支持" {
        fmt.Println("技术支持处理请求:", request)
    } else if t.next != nil {
        t.next.HandleRequest(request)
    }
}

// Concrete handler - billing inquiry handler
type BillingHandler struct {
    next Handler
}

func (b *BillingHandler) SetNext(handler Handler) {
    b.next = handler
}

func (b *BillingHandler) HandleRequest(request string) {
    if request == "账单查询" {
        fmt.Println("账单查询处理请求:", request)
    } else if b.next != nil {
        b.next.HandleRequest(request)
    }
}

// Concrete handler - customer service handler
type CustomerServiceHandler struct {
    next Handler
}

func (c *CustomerServiceHandler) SetNext(handler Handler) {
    c.next = handler
}

func (c *CustomerServiceHandler) HandleRequest(request string) {
    if request == "客户服务" {
        fmt.Println("客户服务处理请求:", request)
    } else if c.next != nil {
        c.next.HandleRequest(request)
    }
}

func main() {
    // create the handler chain
    techSupport := &TechSupportHandler{}
    billing := &BillingHandler{}
    customerService := &CustomerServiceHandler{}

    techSupport.SetNext(billing)
    billing.SetNext(customerService)

    // customer requests
    requests := []string{"技术支持", "账单查询", "客户服务", "其他请求"}

    for _, request := range requests {
        fmt.Println("处理请求:", request)
        techSupport.HandleRequest(request)
        fmt.Println()
    }
}
```

#### Use cases
- You need to handle many different types of requests, and those requests can be handled by multiple handler objects.
- The request-handling logic can be adjusted dynamically, for example choosing a different handler based on different conditions.
- You need to decouple request handling to make the system easier to extend and maintain.

#### Implementation
Implementation takes three steps: the interface declares "set next" and "handle request"; each concrete handler writes its own check and forwards unrecognized requests to `next`; the client is responsible for creating the objects, chaining them together with `SetNext` in order, and then issuing requests.

#### Pros and cons
**Pros**:
- The sender and receiver of a request are decoupled, making the system more flexible to extend and maintain.
- You can dynamically adjust the order of the handler chain or add new handlers.
- Keeps request handling separated and centrally managed.

**Cons**:
- Debugging can be harder, because the request handler chain is dynamic and may involve multiple handlers.
- If the handler chain is long, it can add latency to request handling.

#### Relationship to other patterns
The Strategy pattern defines a family of interchangeable algorithms, while the Chain of Responsibility passes a request along a chain, where each link can use its own strategy. The Command pattern encapsulates a request as an object, and those objects make a natural payload to pass along the chain. The Mediator pattern collapses many-to-many interaction between objects into a single mediator, and once interactions get too complex to fit into a single chain, it is time to switch to a mediator.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Builder](/dp/Builder.md)
- [Command](/dp/Command.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Builder](/dp/Builder.md)
- [Command](/dp/Command.md)
