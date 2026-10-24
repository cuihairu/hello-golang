### Timers and tickers

In Go, both timers and tickers come from the `time` package: a timer (`time.Timer`) handles a single delay, and a ticker (`time.Ticker`) handles periodic repetition. The names are close, but the uses differ.

#### 1. Timers

`time.Timer` is a type in Go's `time` package that runs an operation once after a specified time. It is used to set up a single delay.

- **Main features**:
  - Execute an operation once after a delay
  - Fire an event after waiting for a specified interval

- **Creating a timer**:
  The `time.NewTimer` function creates a new timer that fires after the specified interval.

- **Main methods**:
  - `Stop()`: stops the timer. If it has not fired yet, calling this method cancels the firing.
  - `Reset(d time.Duration)`: resets the timer, setting its interval to a new value.

- **Example code**:

  ```go
  package main

  import (
      "fmt"
      "time"
  )

  func main() {
      // create a timer
      timer := time.NewTimer(2 * time.Second)

      // wait for the timer to fire
      <-timer.C
      fmt.Println("定时器触发了")

      // create a timer and stop it right away
      timer2 := time.NewTimer(1 * time.Second)
      timer2.Stop() // stop the timer immediately

      // try to receive the timer's fire signal
      select {
      case <-timer2.C:
          fmt.Println("定时器2触发了")
      default:
          fmt.Println("定时器2被停止了")
      }
  }
  ```

#### 2. Tickers

`time.Ticker` is a type in Go's `time` package that runs operations periodically. It fires events repeatedly at a specified interval, which suits scenarios where some task must run again and again.

- **Main features**:
  - Fire operations repeatedly at a specified interval
  - Can be used for scheduled tasks and periodic events

- **Creating a ticker**:
  The `time.NewTicker` function creates a new ticker that fires repeatedly at the specified interval.

- **Main methods**:
  - `Stop()`: stops the ticker, canceling its subsequent firings.

- **Example code**:

  ```go
  package main

  import (
      "fmt"
      "time"
  )

  func main() {
      // create a ticker that fires once per second
      ticker := time.NewTicker(1 * time.Second)
      quit := make(chan struct{})

      go func() {
          for {
              select {
              case t := <-ticker.C:
                  fmt.Println("计时器触发时间:", t)
              case <-quit:
                  ticker.Stop()
                  return
              }
          }
      }()

      // stop the ticker after 5 seconds
      time.Sleep(5 * time.Second)
      quit <- struct{}{}
      fmt.Println("计时器停止了")
  }
  ```

#### 3. Differences between timers and tickers

- **How they fire**:
  - **Timer**: fires only once, running an operation after the specified time.
  - **Ticker**: fires periodically, repeating the operation at the specified interval.

- **When to use them**:
  - **Timer**: for one-off tasks, such as running an operation after a delay.
  - **Ticker**: for periodic tasks, such as refreshing state or polling on a schedule.

- **How they work**:
  - **Timer**: receives a one-off fire signal via `<-time.Timer.C`.
  - **Ticker**: receives periodic fire signals via `<-time.Ticker.C`, and stops with `Stop()`.

#### 4. Practical scenarios

- **Timers**:
  - Delayed task execution: for example, retrying after a request times out.
  - Delayed message sending: for example, postponing a confirmation email.

- **Tickers**:
  - Scheduled tasks: for example, checking service health on a schedule.
  - Periodic events: for example, updating an app's UI or data at fixed intervals.

### Summary

Pick by cadence: for a single wait, use `Timer`, take the signal from `<-timer.C`, and call `Stop()` when you no longer need it. For repeats at a fixed interval, use `Ticker` — and still call `Stop()` when done, or the events keep coming. Timeout retries belong to `Timer`; scheduled polling and state refresh belong to `Ticker`.

## References

- [time standard library](https://pkg.go.dev/time)


## Sibling pages

- [Advanced](/time/Advanced.md)
- [ConceptTime](/time/ConceptTime.md)
- [FormatAndParse](/time/FormatAndParse.md)
- [TimeZone](/time/TimeZone.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [TimeZone](/time/TimeZone.md)
