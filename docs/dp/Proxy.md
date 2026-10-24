### Proxy Pattern

#### Intent
The Proxy Pattern is a structural design pattern: it introduces an intermediary object (the proxy); the client accesses the proxy, and the proxy controls access to the real object.

#### Problem
In the real world, consider an image-processing application. Loading a large image can consume a lot of memory and processing time. Loading these images directly can cause performance problems. Here you can use the Proxy Pattern to defer loading the image until it is actually needed.

#### Solution
The approach is to build a proxy class with the same interface as the real object, putting lazy loading and access control in the proxy.

#### Structure
1. **Subject**: defines the shared interface for the proxy and the real object.
2. **RealSubject**: implements the Subject interface and defines the actual business logic.
3. **Proxy**: implements the Subject interface, holds a reference to the real subject, and controls access to the real subject.

#### Code
Go implementation of the Proxy Pattern:

```go
package main

import "fmt"

// Subject interface
type Subject interface {
    Request() string
}

// RealSubject - image
type RealImage struct {
    filename string
}

func (i *RealImage) Request() string {
    return "load image: " + i.filename
}

// Proxy - image proxy
type ProxyImage struct {
    realImage *RealImage
    filename  string
}

func (p *ProxyImage) Request() string {
    if p.realImage == nil {
        // lazy loading
        p.realImage = &RealImage{filename: p.filename}
    }
    return p.realImage.Request()
}

func main() {
    proxyImage := &ProxyImage{filename: "large_image.jpg"}

    // the image is not loaded yet
    fmt.Println("image request:", proxyImage.Request())

    // the image is already loaded
    fmt.Println("image request:", proxyImage.Request())
}
```

#### Applicable scenarios
- You need to control access to an object, especially when lazy loading or access security is required.
- You need a virtual proxy for an object, to avoid creating expensive or time-consuming object instances.
- You need a remote proxy for a real object, to deal with the issues of remote access.

#### Implementation
1. Define the Subject interface, declaring the operations shared by the proxy and the real object.
2. Create the RealSubject class, implementing the Subject interface and defining the actual business logic.
3. Create the Proxy class, holding a reference to the real subject and implementing the Subject interface. In the proxy class you can implement lazy loading, access control, and so on.
4. The client code accesses the real object through the proxy.

#### Pros and cons
**Pros**:
- Gives you control over the real object, including lazy loading and security control.
- Provides a unified interface for accessing the real object.
- Can add functionality to the object, such as caching and logging.

**Cons**:
- Can add complexity to the system, especially in coordinating between the proxy and the real object.
- Can introduce extra performance overhead, especially with complex proxy logic.

#### Relationship to other patterns
- **Decorator Pattern**: similar structure — the decorator adds responsibilities, the proxy controls access. The two can stack; for example the proxy handles lazy loading while the decorator adds functionality.
- **Flyweight Pattern**: the flyweight shares many similar objects to save memory, while the proxy manages access to a single object — you can go through the proxy to fetch a flyweight object.
- **Facade Pattern**: the facade provides a single unified entry point to a whole subsystem, while the proxy only manages access to one real object.

## References

- [GoF "Design Patterns" Overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru Design Patterns Catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Prototype](/dp/Prototype.md)
- [Reactor](/dp/Reactor.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Prototype](/dp/Prototype.md)
- [Reactor](/dp/Reactor.md)
