`expvar` is a package in the Go standard library that exposes runtime variables and statistics of a program as JSON, for monitoring and debugging.

### Main features

- **Runtime statistics**: Data such as request counts, error counts, and memory usage update as the program runs.
- **HTTP exposure**: The data is mounted on an HTTP service; hit `/debug/vars` to fetch it.

### How to use it

#### 1. **Import the `expvar` package**

```go
import (
    "expvar"
    "net/http"
)
```

#### 2. **Define and register variables**

`expvar` provides variables of types `Int`, `Float`, `String`, and `Map`, which you can use to record all kinds of statistics. For example:

```go
import (
    "expvar"
    "net/http"
)

var (
    requestCount = expvar.NewInt("request_count")
    errorCount   = expvar.NewInt("error_count")
    version      = expvar.NewString("version")
)

func main() {
    version.Set("1.0.0")  // set the application version

    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        requestCount.Add(1) // increment the request count
        // simulate request handling
        w.Write([]byte("Hello, world!"))
    })

    http.ListenAndServe(":8080", nil)
}
```

#### 3. **Using the `Map` type**

`Map` groups several related metrics together, and is exported as JSON just like the others. For example:

```go
import (
    "expvar"
    "net/http"
)

var metrics = expvar.NewMap("metrics")

func main() {
    metrics.Set("requests", expvar.NewInt("requests"))
    metrics.Set("errors", expvar.NewInt("errors"))

    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        metrics.Get("requests").(*expvar.Int).Add(1)
        // simulate request handling
        w.Write([]byte("Hello, world!"))
    })

    http.ListenAndServe(":8080", nil)
}
```

#### 4. **Viewing `expvar` data**

Once your application is running, visit `http://localhost:8080/debug/vars` to see the exported variables. `expvar` returns the data as JSON, for example:

```json
{
    "request_count": 100,
    "error_count": 5,
    "version": "1.0.0",
    "metrics": {
        "requests": 100,
        "errors": 5
    }
}
```

### Advanced usage

- **Custom types**: Implement the `expvar.Var` interface to export a type you wrote yourself.

- **Integrating monitoring**: Monitoring systems such as Prometheus can scrape `expvar` data over the HTTP endpoint.

### Notes

- **Security**: The endpoint `expvar` exposes may contain sensitive information, so put access control on `debug/vars` in production.

- **Performance**: It suits low-frequency statistics. When updates are very frequent, switch to a more specialized monitoring tool.

If you want to add a few runtime counters to a program quickly, `expvar` is the ready-made option that ships with the standard library, with no third-party dependency.

## References

- [Official · Diagnostics](https://go.dev/doc/diagnostics)
- [runtime/pprof standard library](https://pkg.go.dev/runtime/pprof)
- [expvar standard library](https://pkg.go.dev/expvar)


## Sibling pages

- [PGO](/debug/PGO.md)
- [Pprof](/debug/Pprof.md)
- [Debug](/debug/Debug.md)
- [Delve](/debug/Delve.md)
- [GDB](/debug/GDB.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [GDB](/debug/GDB.md)
