`ErrorGroup` is a Go synchronization primitive that behaves like `sync.WaitGroup`, but adds error aggregation: it is provided by `errgroup` in the `golang.org/x/sync` package, and it records and returns the first error while waiting for a group of goroutines.

### 1. Basic Functionality

The basic capabilities of `ErrorGroup` are:

- **Waiting for all goroutines to finish**: like `sync.WaitGroup`, `ErrorGroup` can wait for a group of goroutines to complete.
- **Capturing the first error**: in concurrent tasks, if any task returns an error, `ErrorGroup` records that error (keeping only the first one), and if it was created with `errgroup.WithContext` it cancels the associated context so the other tasks have a chance to exit early. Note that `Wait` still waits for every goroutine to finish.
- **Returning the first error**: `ErrorGroup` returns the first error that occurred, letting the caller handle or report it.

### 2. Example

The following example uses `ErrorGroup` to launch multiple goroutines and collect any errors that occur.

```go
package main

import (
	"context"
	"fmt"
	"time"

	"golang.org/x/sync/errgroup"
)

func main() {
	// create an ErrorGroup with cancellation via WithContext
	g, ctx := errgroup.WithContext(context.Background())

	for i := 1; i <= 3; i++ {
		i := i // Capture loop variable
		g.Go(func() error {
			select {
			case <-ctx.Done(): // cancellation fires when another task fails
				fmt.Printf("Goroutine %d canceled\n", i)
				return ctx.Err()
			case <-time.After(time.Second * time.Duration(i)):
			}
			if i == 2 {
				return fmt.Errorf("error from goroutine %d", i)
			}
			fmt.Printf("Goroutine %d completed successfully\n", i)
			return nil
		})
	}

	// Wait returns the first non-nil error after all goroutines finish
	if err := g.Wait(); err != nil {
		fmt.Printf("Error occurred: %v\n", err)
	}
}
```

### 3. How It Works

#### 3.1 The `errgroup.Group` Struct

`errgroup.Group` uses `sync.WaitGroup` internally to synchronize goroutine execution, and `sync.Once` to make sure only the first error is recorded. Here is the simplified internal structure (details such as the semaphore used by `SetLimit` are omitted for readability):

```go
package errgroup

import "sync"

// Group represents a set of goroutines working toward a common goal.
type Group struct {
    cancel func(error) // cancel function injected when the Group is created; nil means not cancellable
    errOnce sync.Once  // guarantees only the first error is recorded
    err     error
    wg      sync.WaitGroup
}

// Go starts a new goroutine and adds it to the group.
func (g *Group) Go(f func() error) {
    g.wg.Add(1)
    go func() {
        defer g.wg.Done()
        if err := f(); err != nil {
            g.errOnce.Do(func() {
                g.err = err
                if g.cancel != nil {
                    g.cancel(err)
                }
            })
        }
    }()
}

// Wait waits for all goroutines to finish and returns the first non-nil error encountered.
func (g *Group) Wait() error {
    g.wg.Wait()
    return g.err
}
```

#### 3.2 The `Go` Method

The `Go` method starts a new goroutine and adds it to the `ErrorGroup`. It checks for an error once the goroutine completes, records the first one it finds, and cancels the other goroutines' execution at the same time (if a cancel function was provided).

#### 3.3 The `Wait` Method

The `Wait` method waits for every goroutine to finish and returns the first non-`nil` error. If no error occurred, it returns `nil`.

### 4. Caveats and Common Problems

#### 4.1 Error Handling

After finding the first error, `ErrorGroup` does not forcibly terminate the other goroutines — a goroutine cannot be killed directly from outside. If you created a cancellable context with `errgroup.WithContext`, it will cancel that context, but the other goroutines need to watch `ctx.Done()` themselves and return as soon as they can; goroutines that do not watch the context keep running until the end. Also, `Wait` always returns only after every goroutine has finished.

#### 4.2 Concurrency Safety

`errgroup.Group` uses a mutex to protect access to the error variable, ensuring it is safe in a concurrent environment. Even so, when using `ErrorGroup` you still need to make sure any other shared resources are concurrency-safe.

#### 4.3 Using `context`

`ErrorGroup` can be paired with `context.Context` to cancel running goroutines when an error occurs. Pass the right context at creation time and you can actually manage the goroutines' lifetimes.

### Summary

`ErrorGroup` folds "wait for a group of goroutines" and "aggregate the first error" into a single step: `Go` submits tasks, `Wait` returns the first non-`nil` error. Paired with `errgroup.WithContext`, the first failing task cancels the associated context, and the remaining tasks that watch `ctx.Done()` can exit early. Compared with waiting on `sync.WaitGroup` and then adding your own locking to record errors, this API saves a fair amount of boilerplate.

## References

- [Effective Go · Concurrency](https://go.dev/doc/effective_go#concurrency)
- [Go Memory Model](https://go.dev/ref/mem)
- [sync standard library](https://pkg.go.dev/sync)
- [golang.org/x/sync/errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Concurrency](/concurrency/Concurrency.md)
- [glossary](/glossary.md)
