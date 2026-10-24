One step further with time handling: high-precision timing, timezone conversion, scheduled tasks, and parsing and formatting time strings. Below is a code sample for each scenario.

### 1. High-precision time measurement

Go's `time` package provides high-precision time measurement, suitable for performance analysis and exact timing. `time.Now()` and `time.Since()` do the measuring.

- **Example code**:
  ```go
  package main

  import (
      "fmt"
      "time"
  )

  func main() {
      start := time.Now()

      // perform the timed operation
      time.Sleep(2 * time.Second)

      elapsed := time.Since(start)
      fmt.Printf("操作耗时: %v\n", elapsed)
  }
  ```

### 2. Time series analysis

Working with time series data (logs, sensor readings) means sorting, aggregating and analyzing records in chronological order. Go's time functions handle all of it.

- **Sorting by time**:
  ```go
  package main

  import (
      "fmt"
      "sort"
      "time"
  )

  type Event struct {
      Time time.Time
      Data string
  }

  func main() {
      events := []Event{
          {Time: time.Now().Add(-5 * time.Hour), Data: "Event1"},
          {Time: time.Now().Add(-1 * time.Hour), Data: "Event2"},
          {Time: time.Now().Add(-3 * time.Hour), Data: "Event3"},
      }

      // sort by time
      sort.Slice(events, func(i, j int) bool {
          return events[i].Time.Before(events[j].Time)
      })

      for _, event := range events {
          fmt.Println(event.Time, event.Data)
      }
  }
  ```

### 3. Timezone conversion and handling

Cross-timezone applications have to deal with local time in different regions. That means converting and computing across timezones, which `time.LoadLocation` and `time.In` cover.

- **Example code**:
  ```go
  package main

  import (
      "fmt"
      "time"
  )

  func main() {
      utcTime := time.Now().UTC()
      fmt.Println("UTC时间:", utcTime)

      // convert to the New York timezone
      nyLocation, _ := time.LoadLocation("America/New_York")
      nyTime := utcTime.In(nyLocation)
      fmt.Println("纽约时间:", nyTime)

      // convert to the Shanghai timezone
      shLocation, _ := time.LoadLocation("Asia/Shanghai")
      shTime := utcTime.In(shLocation)
      fmt.Println("上海时间:", shTime)
  }
  ```

### 4. Scheduled task dispatch

`time.Timer` and `time.Ticker` cover one-off and periodic tasks. Pair them with `select` and channels for more complex scheduling.

- **Example code**:
  ```go
  package main

  import (
      "fmt"
      "time"
  )

  func main() {
      ticker := time.NewTicker(1 * time.Second)
      stop := make(chan bool)

      go func() {
          for {
              select {
              case <-ticker.C:
                  fmt.Println("每秒执行一次")
              case <-stop:
                  ticker.Stop()
                  return
              }
          }
      }()

      // stop after running for 5 seconds
      time.Sleep(5 * time.Second)
      stop <- true
      fmt.Println("停止了定时任务")
  }
  ```

### 5. Time parsing and formatting

`time.Parse` and `time.Format` handle parsing and formatting complex time strings, including custom layouts.

- **Example code**:
  ```go
  package main

  import (
      "fmt"
      "time"
  )

  func main() {
      layout := "2006-01-02 15:04:05"
      timeStr := "2024-07-27 15:30:00"

      // parse the time string
      parsedTime, err := time.Parse(layout, timeStr)
      if err != nil {
          fmt.Println("解析错误:", err)
          return
      }
      fmt.Println("解析后的时间:", parsedTime)

      // format the time
      formattedTime := parsedTime.Format("Mon Jan 2 15:04:05 MST 2006")
      fmt.Println("格式化后的时间:", formattedTime)
  }
  ```

### 6. Converting timestamps and time points

A timestamp counts seconds since the epoch (00:00:00 UTC on 1 January 1970). `time.Unix` and `time.Time.Unix` convert between timestamps and time points.

- **Example code**:
  ```go
  package main

  import (
      "fmt"
      "time"
  )

  func main() {
      // current timestamp
      currentTimestamp := time.Now().Unix()
      fmt.Println("当前时间戳:", currentTimestamp)

      // create a time from a timestamp
      timestamp := time.Unix(currentTimestamp, 0)
      fmt.Println("从时间戳创建的时间:", timestamp)
  }
  ```

### 7. Computing and comparing durations

Compute durations and compare times; the `time.Duration` type does the exact interval work.

- **Example code**:
  ```go
  package main

  import (
      "fmt"
      "time"
  )

  func main() {
      start := time.Now()
      time.Sleep(2 * time.Second)
      end := time.Now()

      duration := end.Sub(start)
      fmt.Printf("时间间隔: %v\n", duration)

      // compare two times
      if end.After(start) {
          fmt.Println("结束时间在开始时间之后")
      }
  }
  ```

### Summary

These operations cluster into a few groups: `time.Now()` and `time.Since()` for timing, `time.LoadLocation` and `In` for timezones, `Parse` and `Format` for string conversion, `Timer`/`Ticker` for scheduling, the `Unix` family for timestamps, `Duration` for interval math. Pick whichever fits.

## References

- [time standard library](https://pkg.go.dev/time)

## Sibling pages

- [ConceptTime](/time/ConceptTime.md)
- [FormatAndParse](/time/FormatAndParse.md)
- [PkgTime](/time/PkgTime.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ConceptTime](/time/ConceptTime.md)
- [FormatAndParse](/time/FormatAndParse.md)
- [PkgTime](/time/PkgTime.md)
- [Practice](/time/Practice.md)
- [TimeZone](/time/TimeZone.md)
- [TimerAndTicker](/time/TimerAndTicker.md)
