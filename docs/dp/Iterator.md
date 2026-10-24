### Iterator Pattern

#### Intent
The Iterator pattern is a behavioral design pattern that provides a way to access the elements of an aggregate object sequentially without exposing its internal representation. By introducing an iterator object, it lets clients traverse the elements of an aggregate without knowing the aggregate's concrete implementation.

#### Problem
In the real world, consider a shopping cart application whose cart holds all kinds of items. We want to iterate over the items in the cart without exposing the cart's internal implementation. Exposing the internals directly would introduce coupling and unnecessary complexity.

#### Solution
With the Iterator pattern, we can define an iterator interface and create concrete iterator classes that implement it. The iterator object accesses the elements of the aggregate sequentially, while the aggregate object only needs to provide a method that creates an iterator.

#### Pattern structure
1. **Iterator**: defines the interface for traversing the aggregate, including methods such as getting the next element and checking whether there is a next element.
2. **Concrete Iterator**: implements the Iterator interface and provides the concrete traversal logic for the aggregate.
3. **Aggregate**: defines a method for creating iterators.
4. **Concrete Aggregate**: implements the Aggregate interface, stores the elements of the collection, and provides a method for creating concrete iterators.

#### Code
Here is an example of the Iterator pattern implemented in Go:

```go
package main

import "fmt"

// Iterator interface
type Iterator interface {
    HasNext() bool
    Next() interface{}
}

// Aggregate interface
type Aggregate interface {
    CreateIterator() Iterator
}

// Concrete Aggregate - shopping cart
type ShoppingCart struct {
    items []string
}

func (s *ShoppingCart) AddItem(item string) {
    s.items = append(s.items, item)
}

func (s *ShoppingCart) CreateIterator() Iterator {
    return &ShoppingCartIterator{cart: s, index: 0}
}

// Concrete Iterator - shopping cart iterator
type ShoppingCartIterator struct {
    cart  *ShoppingCart
    index int
}

func (i *ShoppingCartIterator) HasNext() bool {
    return i.index < len(i.cart.items)
}

func (i *ShoppingCartIterator) Next() interface{} {
    item := i.cart.items[i.index]
    i.index++
    return item
}

func main() {
    cart := &ShoppingCart{}
    cart.AddItem("Apple")
    cart.AddItem("Banana")
    cart.AddItem("Cherry")

    iterator := cart.CreateIterator()

    fmt.Println("购物车中的商品:")
    for iterator.HasNext() {
        item := iterator.Next()
        fmt.Println(item)
    }
}
```

#### Applicable scenarios
- You need to access the elements of a collection object without exposing the collection's internal representation.
- You need to support multiple traversal modes, such as forward and backward traversal.
- You need to support concurrent operations during traversal.

#### Implementation
1. Define the Iterator interface, declaring the operations for traversing the aggregate.
2. Create a concrete iterator class that implements the Iterator interface and defines the concrete traversal logic.
3. Define the Aggregate interface, declaring a method for creating iterators.
4. Create a concrete aggregate class that implements the Aggregate interface, stores the elements of the collection, and provides a method for creating concrete iterators.
5. Clients traverse the elements of the collection through the iterator object without needing to care about the collection's internal implementation.

#### Pros and cons
**Pros**:
- The operation of traversing collection elements is decoupled from the collection's implementation; clients do not need to know the collection's internal structure.
- You can provide multiple traversal modes for a collection and support different traversal strategies.
- It supports modifying the collection dynamically during traversal.

**Cons**:
- It may introduce additional classes, increasing system complexity.
- If the collection is very large, the iterator's implementation may increase memory usage.

#### Relationship to other patterns
- **Iterator Pattern and Composite Pattern**: Composite combines objects into a tree structure to represent a "part-whole" hierarchy, while Iterator traverses the elements of a collection. Iterator can be used together with Composite to traverse the tree structure of Composite.
- **Iterator Pattern and Observer Pattern**: Observer notifies observers when an object's state changes, while Iterator traverses the elements of a collection. The two can be combined, for example observing and handling element state changes during traversal.
- **Iterator Pattern and Chain of Responsibility Pattern**: Chain of Responsibility passes requests along a chain, while Iterator traverses the elements of a collection. They can be combined, for example passing requests along the chain of responsibility during iteration.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Flyweight](/dp/Flyweight.md)
- [Mediator](/dp/Mediator.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Flyweight](/dp/Flyweight.md)
- [Mediator](/dp/Mediator.md)
