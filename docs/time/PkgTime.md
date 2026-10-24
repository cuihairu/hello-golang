### Introduction to the `time` package

Go's standard library `time` package handles fetching, creating, formatting, parsing, timezones, and timers for time and dates.

#### 2.1 What the `time` package does

The main responsibilities of the `time` package:

- **Get the current time**: provides methods to obtain the current time and date.
- **Create time values**: supports creating `Time` values for a specified date and time.
- **Format and parse time**: can format a time as a string, and parse a string into a time.
- **Time arithmetic**: supports adding to and subtracting from time, comparing times, and computing intervals.
- **Timers and tickers**: provides the `Timer` and `Ticker` types for one-off delays and periodic events.
- **Timezone handling**: supports loading timezones and converting a time into a given timezone.

#### 2.2 Installing and importing the `time` package

In Go, the `time` package is part of the standard library and needs no separate installation. To use it, just import it in your code:

```go
import "time"
```

#### Overview of common features

1. **The `time.Time` type**:
   - Represents a specific point in time.
   - Provides many methods to manipulate time and retrieve its parts, such as year, month, day, hour, minute, and second.

2. **Formatting and parsing time**:
   - Use the `Format` method to convert a `time.Time` to a string.
   - Use the `Parse` method to parse a time string into a `time.Time` value.
   - Time formats are defined against a fixed layout (`2006-01-02 15:04:05`).

3. **Timezone handling**:
   - The `LoadLocation` method loads a timezone.
   - The `In` method converts a time into a specified timezone.

4. **Time arithmetic**:
   - The `Add` method adds a duration to a time.
   - The `Sub` method computes the difference between two points in time.

5. **Timers and tickers**:
   - The `Timer` type is for one-off timed events.
   - The `Ticker` type is for periodic timed events.
   - The `Sleep` function pauses the current goroutine for a specified duration.

#### Example code

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // get the current time
    now := time.Now()
    fmt.Println("当前时间:", now)

    // create a specific time
    date := time.Date(2024, time.July, 27, 15, 30, 0, 0, time.UTC)
    fmt.Println("指定日期时间:", date)

    // format time
    formatted := now.Format("2006-01-02 15:04:05")
    fmt.Println("格式化后的时间:", formatted)

    // parse time
    layout := "2006-01-02 15:04:05"
    value := "2024-07-27 15:30:00"
    t, err := time.Parse(layout, value)
    if err != nil {
        fmt.Println("解析错误:", err)
    } else {
        fmt.Println("解析后的时间:", t)
    }

    // use a timer
    timer := time.NewTimer(2 * time.Second)
    go func() {
        t := <-timer.C
        fmt.Println("定时器触发时间:", t)
    }()

    // use a ticker
    ticker := time.NewTicker(1 * time.Second)
    go func() {
        for t := range ticker.C {
            fmt.Println("Tick at", t)
        }
    }()

    // pause execution
    time.Sleep(5 * time.Second)
    ticker.Stop()
}
```

### Summary

Keep a few of the common ones in mind: formatting uses the fixed layout `2006-01-02 15:04:05`, moving forward or backward uses `Add`, intervals use `Sub`, one-off delays use `Timer`, and periodic tasks use `Ticker`.

## References

- [time standard library](https://pkg.go.dev/time)

## Sibling pages

- [Advanced](/time/Advanced.md)
- [ConceptTime](/time/ConceptTime.md)
- [FormatAndParse](/time/FormatAndParse.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/time/Advanced.md)
- [ConceptTime](/time/ConceptTime.md)
- [FormatAndParse](/time/FormatAndParse.md)
- [Practice](/time/Practice.md)
