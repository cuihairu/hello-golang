# The blank identifier

`_` is the blank identifier in Go. It can appear in a declaration or assignment just like any ordinary identifier, but every value assigned to it is discarded immediately. It takes no memory and cannot be referenced by later code. The blank identifier is the foundation of Go's "explicitly ignore" idiom.

### Basic uses

#### 1. Ignoring part of a function's return values

Go functions often return multiple values. When you only need part of them, use `_` to explicitly ignore the rest:

```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	// only care about the conversion result, ignore the error (when the input is known to be valid)
	n, _ := strconv.Atoi("42")
	fmt.Println(n * 2) // prints: 84

	// only care about the index, ignore the value
	s := []string{"a", "b", "c"}
	for i, _ := range s {
		fmt.Print(i, " ")
	}
	fmt.Println()
}
```

#### 2. Ignoring the key or value in range

When you don't need one of the iteration values, use `_` in its place:

```go
numbers := []int{1, 2, 3}
sum := 0
for _, v := range numbers { // ignore the index, only take the value
	sum += v
}
```

In practice, when the loop body only uses the index, it's conventional to write `for i := range s` directly — it means the same thing as `for i, _ := range s` and is more concise.

#### 3. Triggering a package's side-effect initialization

This is one of the most important uses of the blank identifier. When you import a package without directly using any of its identifiers, you must prefix it with `_`, or you get a compile error. A typical example is registering a database driver:

```go
import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql" // only to run the package's init(), registering the mysql driver
)

func main() {
	// the driver is already registered in init, so "mysql" can be used directly here
	db, err := sql.Open("mysql", "user:password@/dbname")
	if err != nil {
		panic(err)
	}
	defer db.Close()
}
```

`database/sql` decouples concrete drivers through a driver registry: a driver package's `init()` calls `sql.Register` to complete the registration, and application code only depends on the `database/sql` interface.

#### 4. "Check but don't use" in a type assertion

In a `switch` or a type assertion, use `_` to say you don't care about the concrete value:

```go
v := interface{}("hello")

// whether the assertion succeeds, without using the value
if _, ok := v.(string); ok {
	fmt.Println("v is a string")
}
```

#### 5. Forcing a compile-time check in a declaration

The rules that "constant/variable declarations must be used" and "imports must be used" let you use the blank identifier for compile-time assertions. A common trick in the standard library is to make a type implement an interface:

```go
package main

import "fmt"

type Shape interface {
	Area() float64
}

type Square struct{ Side float64 }

func (s Square) Area() float64 { return s.Side * s.Side }

// compile-time assertion: *Square must implement Shape, or it won't compile
var _ Shape = (*Square)(nil)

func main() {
	var s Shape = &Square{Side: 3}
	fmt.Println(s.Area()) // prints: 9
}
```

If `Square`'s `Area` method is later deleted or renamed, the line `var _ Shape = (*Square)(nil)` fails immediately at compile time, instead of being caught only at run time.

#### 6. Ignoring assignment results you don't need

```go
package main

import "fmt"

func main() {
	// ignore the second return value when reading a map (whether the key exists)
	m := map[string]int{"a": 1}
	v, _ := m["a"] // only want the value, don't care whether the key exists (v is the zero value when it doesn't)
	fmt.Println(v)  // prints: 1

	// don't care about the value (unlike m["a"], which yields the zero value when the key is missing — use this only to check whether the value is the zero value)
	_, exists := m["b"]
	fmt.Println(exists) // prints: false
}
```

### The blank identifier vs. unused variables

Be careful to distinguish two cases:

- **A variable declared but not used** (after `x := 10`, `x` is never read) is a compile error. When you temporarily don't need it, you can write `_ = x` to explicitly "use" it (very common when debugging).
- **Assigning to `_`** is always legal, because `_` is not a newly declared variable and does not need to be used.

```go
func f() (int, error) { return 1, nil }

func main() {
	x, _ := f() // legal
	_ = x       // if x isn't needed for now, use the blank identifier to explicitly discard it
}
```

### Usage notes

- **Don't overuse `_` to swallow errors**: ignoring an error means that when it happens, the program keeps running with a corrupt intermediate state — the root of many production incidents. Only ignore it when you're sure the failure doesn't matter (or has been logged elsewhere).
- **`_` cannot appear in a use position**: `fmt.Println(_)` is illegal. The blank identifier can only "catch" a value being discarded in an assignment/declaration statement; it can't be referenced as an expression.

### Summary

The blank identifier is Go's standard way of saying "I know there's a value here, but I'm deliberately not using it": ignoring surplus return values, importing a side-effect-only package, writing a compile-time interface assertion. Used properly, it makes intent obvious at a glance. Used carelessly — especially swallowing errors — it plants a landmine.

## References

- [Effective Go (official)](https://go.dev/doc/effective_go)
- [Effective Go · blank](https://go.dev/doc/effective_go#blank)

## Sibling pages

- [EffectiveGo](/idioms/EffectiveGo.md)
- [StructTags](/idioms/StructTags.md)
- [CommaOk](/idioms/CommaOk.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [CommaOk](/idioms/CommaOk.md)
- [Idioms](/idioms/Idioms.md)
- [Labels](/idioms/Labels.md)
- [Range](/idioms/Range.md)
- [ShortVarDecl](/idioms/ShortVarDecl.md)
