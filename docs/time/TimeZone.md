### Timezone handling

Go's `time` package owns timezones: loading (`LoadLocation`), conversion (`In`), and daylight saving driven by the timezone database. When displaying time across timezones, fix the timezone on the `time.Time` value first, then do the arithmetic.

#### 5.1 Timezone basics

A timezone defines the offset between a region's local time and Coordinated Universal Time (UTC). A timezone includes not only the offset (for example `+08:00`) but may also include daylight saving (DST) rules.

- **Timezone offset**: the offset of that timezone relative to UTC. For example, `UTC+08:00` means eight hours ahead of UTC.
- **Daylight Saving Time (DST)**: some regions adjust the time in certain seasons to make better use of daylight. Go supports these adjustments through the timezone database.

#### 5.2 Loading timezones

Go loads timezone information with the `time.LoadLocation` function. Timezone information usually comes from the operating system or the timezone database.

- **Loading a timezone**:
  ```go
  location, err := time.LoadLocation("America/New_York")
  if err != nil {
      fmt.Println("加载时区失败:", err)
  } else {
      fmt.Println("加载的时区:", location)
  }
  ```

- **Predefined timezones**:
  Go's `time` package provides a few predefined timezones, such as `UTC`. You can use these directly for time calculations.

#### 5.3 Converting time

Converting time from one timezone to another usually involves changing the timezone part of a `time.Time` value to the new timezone.

- **Converting timezones**:
  ```go
  now := time.Now()
  fmt.Println("当前时间:", now)

  // load the target timezone
  location, err := time.LoadLocation("Asia/Shanghai")
  if err != nil {
      fmt.Println("加载时区失败:", err)
      return
  }

  // convert the current time to the target timezone
  shanghaiTime := now.In(location)
  fmt.Println("上海时间:", shanghaiTime)
  ```

#### 5.4 Handling daylight saving

Go's `time` package handles daylight saving changes automatically. You only need to load timezone information that includes DST rules, and Go applies those rules as needed.

- **Example**:
  ```go
  location, err := time.LoadLocation("America/New_York")
  if err != nil {
      fmt.Println("加载时区失败:", err)
      return
  }

  // create a time during daylight saving (arguments are: year, month, day, hour, minute, second, nanosecond, timezone)
  summerTime := time.Date(2024, time.July, 1, 12, 0, 0, 0, location)
  fmt.Println("夏令时期间的时间:", summerTime) // 2024-07-01 12:00:00 -0400 EDT
  ```

#### 5.5 Parsing timezone strings

A timezone can also be written as a string, such as `-07:00` or `Z07:00`. Put it in the layout for `time.Parse`, and the parsed time carries the corresponding timezone.

- **Parsing a timezone string**:
  ```go
  layout := "2006-01-02 15:04:05 -07:00"
  value := "2024-07-27 15:30:00 +08:00"
  t, err := time.Parse(layout, value)
  if err != nil {
      fmt.Println("解析错误:", err)
  } else {
      fmt.Println("解析后的时间:", t)
  }
  ```

#### 5.6 Commonly used timezone information

- **`UTC`**: Coordinated Universal Time, unaffected by daylight saving.
- **`Local`**: the system's local timezone.
- **`America/New_York`**: the New York timezone, which includes daylight saving adjustments.
- **`Asia/Shanghai`**: the Shanghai timezone, which usually has no daylight saving.

#### 5.7 The timezone database

Go uses the system timezone database (such as the IANA timezone database), which contains detailed information for timezones worldwide. Timezone database updates come through the operating system's timezone updates.

#### 5.8 Things to watch out for when handling timezones

- **Consistency**: keep times consistent across timezone conversions. Converting everything to UTC before doing calculations avoids problems caused by timezone differences.
- **Daylight saving adjustments**: be aware of the dates when DST starts and ends. Some timezones shift an hour forward or back during DST.
- **Timezone names**: use standard timezone names (such as `America/Los_Angeles`) rather than just an offset (such as `-08:00`), which avoids mistakes around daylight saving changes.

### Summary

Three things for timezones: `time.LoadLocation` loads by IANA name, `t.In(loc)` switches the display timezone, and daylight saving rides along with the timezone database. For cross-timezone arithmetic, normalize to UTC first. Use a name like `America/New_York` instead of `-08:00`, so DST switches don't throw off the math.

## References

- [time standard library](https://pkg.go.dev/time)


## Sibling pages

- [Advanced](/time/Advanced.md)
- [ConceptTime](/time/ConceptTime.md)
- [FormatAndParse](/time/FormatAndParse.md)
- [Practice](/time/Practice.md)
- [TimerAndTicker](/time/TimerAndTicker.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Practice](/time/Practice.md)
- [TimerAndTicker](/time/TimerAndTicker.md)
