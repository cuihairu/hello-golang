### Common pitfalls and best practices

Time handling has plenty of traps: precision, timezones, format layouts, and mixing up timers and tickers. Below are the common problems first, then the matching practices.

### 1. Common problems

#### 1.1 Time precision issues

**Problem**: precision problems in time operations, for example using `time.Sleep` or `time.After` for high-precision timing can cause unexpected delays.

**Solution**: use `time.Now()` and `time.Since()` to measure exact intervals, rather than relying on `time.Sleep` for precise timing. If you need high-precision timing, consider using the `time.Duration` type for time calculations.

#### 1.2 Timezone conversion errors

**Problem**: common timezone conversion mistakes include not accounting for daylight saving (DST) changes, or using wrong timezone names.

**Solution**: always use standard timezone names (such as `America/New_York`) instead of strings that only contain an offset (such as `-08:00`). Make sure to use `time.LoadLocation` to load timezone information, so daylight saving changes are handled automatically.

#### 1.3 Time string parsing errors

**Problem**: when parsing a time string, the format does not match the actual string, causing the parse to fail.

**Solution**: make sure the time string matches the layout template exactly. Go uses the fixed time format `"2006-01-02 15:04:05"` as a reference, and you adjust the layout to fit your actual time string.

#### 1.4 Mixing timers and tickers

**Problem**: mixing up timers and tickers can lead to unexpected behavior, for example using a timer instead of a ticker for repeated work.

**Solution**: use `time.Timer` for one-off delays, and `time.Ticker` for periodic repeated tasks. Understanding the difference helps you pick the right tool.

#### 1.5 Timestamp and time value conversion errors

**Problem**: converting between timestamps and time values can hit timezone-related issues.

**Solution**: when handling timestamps, remember that timestamps are based on UTC. If you need to convert a timestamp to a specific timezone, first convert the timestamp to UTC, then convert to the target timezone as needed.

### 2. Best practices

#### 2.1 Use the time features the standard library provides

**Practice**: the `time` package covers most scenarios. Before writing your own time handling code, check that the standard library has nothing ready-made.

#### 2.2 Use standard timezone names when handling timezones

**Practice**: always use standard timezone names (such as `Asia/Shanghai`, `America/Los_Angeles`) for timezone conversion, rather than strings containing only an offset. Daylight saving changes and regional timezone rules are the library's job — no need to compute them yourself.

#### 2.3 Use `time.Duration` for interval calculations

**Practice**: when computing intervals, represent them with the `time.Duration` type, which makes spans clearer and supports adding to and subtracting from time.

- **Example code**:
  ```go
  package main

  import (
      "fmt"
      "time"
  )

  func main() {
      duration := 2 * time.Hour
      fmt.Println("时间间隔:", duration)
      
      futureTime := time.Now().Add(duration)
      fmt.Println("当前时间加2小时:", futureTime)
  }
  ```

#### 2.4 Handle concurrency with time correctly

**Practice**: when using time-related features in concurrent code, make sure operations on `time.Timer` and `time.Ticker` are thread safe. Use a `select` statement to handle the signals from timers and tickers.

- **Example code**:
  ```go
  package main

  import (
      "fmt"
      "time"
  )

  func main() {
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

      time.Sleep(5 * time.Second)
      quit <- struct{}{}
      fmt.Println("停止了计时器")
  }
  ```

#### 2.5 Handling daylight saving changes

**Practice**: in applications that need to handle daylight saving, make sure to use a timezone that supports DST adjustments, and be aware of the dates when DST starts and ends. Avoid hardcoding DST; use `time.LoadLocation` to load timezone information that supports it.

#### 2.6 High-precision time measurement

**Practice**: for high-precision time measurement, use `time.Now()` and `time.Since()` to get exact intervals, instead of relying on `time.Sleep` for timing.

### Summary

The pitfalls in time handling cluster into three groups: timezones, format layouts, and timers. For timezones, hand the math to the library with IANA names. When parsing, align to the `"2006-01-02 15:04:05"` reference format. Use `Ticker` for periodic tasks and `Timer` for one-off delays.

## References

- [time standard library](https://pkg.go.dev/time)


## Sibling pages

- [Advanced](/time/Advanced.md)
- [ConceptTime](/time/ConceptTime.md)
- [FormatAndParse](/time/FormatAndParse.md)
- [PkgTime](/time/PkgTime.md)
- [TimeZone](/time/TimeZone.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [TimeZone](/time/TimeZone.md)
