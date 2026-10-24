Go's time formatting and parsing differ from most other languages: the layout is defined against a fixed reference point, `2006-01-02 15:04:05`. The main rules:

### Special rules for time formatting and parsing

#### 1. The layout is fixed

Go uses the specific point `2006-01-02 15:04:05` as the reference for time layouts. This means that when formatting or parsing time you must use the structure of that point to define the layout. The reference point is fixed and cannot be changed.

- **Example**:
  - `2006` represents the year
  - `01` represents the month
  - `02` represents the day
  - `15` represents the hour (24-hour clock)
  - `04` represents the minute
  - `05` represents the second

  **Example**:
  ```go
  layout := "2006-01-02 15:04:05"
  fmt.Println(time.Now().Format(layout)) // format the current time with the layout string
  ```

#### 2. Using predefined layouts

The Go standard library provides a set of commonly used predefined time layouts for formatting and parsing. These layouts follow the fixed reference point and are widely used across different scenarios.

- **Common predefined layouts**:
  - `time.RFC3339`: `2006-01-02T15:04:05Z07:00`
  - `time.RFC1123`: `Mon, 02 Jan 2006 15:04:05 MST`
  - `time.RFC850`: `Monday, 02-Jan-06 15:04:05 PST`
  - `time.UnixDate`: `Mon Jan 2 15:04:05 MST 2006`
  - `time.ANSIC`: `Mon Jan _2 15:04:05 2006`

  **Example**:
  ```go
  now := time.Now()
  fmt.Println(now.Format(time.RFC3339)) // format as RFC3339
  ```

#### 3. Special characters in layouts

In a time layout, the meaning of letters and digits is fixed and must match exactly. These characters denote specific parts of the time:

- **Letters**:
  - `Mon`: the day of the week (e.g. Mon)
  - `Jan`: the month (e.g. Jan)
  - `02`: the day of the month (e.g. 02)
  - `15`: the hour (24-hour clock, e.g. 15)
  - `04`: the minute (e.g. 04)
  - `05`: the second (e.g. 05)

- **Special characters**:
  - `-`: the date separator (e.g. `2006-01-02`)
  - `:`: the time separator (e.g. `15:04:05`)
  - `T`: the separator between date and time (e.g. `2006-01-02T15:04:05`)
  - `Z07:00`: represents the timezone (e.g. `Z07:00`)

  **Example**:
  ```go
  customLayout := "2006年01月02日 15时04分05秒"
  fmt.Println(time.Now().Format(customLayout)) // Chinese and punctuation print as-is
  ```

#### 4. Parsing timezones

When parsing a time string, the timezone part must match the timezone format in the layout exactly. Timezone handling in Go follows these rules:

- **Timezone identifiers**: such as `MST`, `UTC`, must be specified correctly in the layout.
- **Offsets**: for example `-07:00`, giving the specific timezone offset.

  **Example**:
  ```go
  layoutWithZone := "2006-01-02 15:04:05 MST"
  valueWithZone := "2024-07-27 15:30:00 UTC"
  tWithZone, err := time.Parse(layoutWithZone, valueWithZone)
  if err != nil {
      fmt.Println("解析错误:", err)
  } else {
      fmt.Println("解析后的时间:", tWithZone)
  }
  ```

#### 5. The zero time

In Go, the zero value of `time.Time` is the "zero time", `0001-01-01 00:00:00 +0000 UTC`. It is a valid time value, typically used to represent an uninitialized time or the default value for time.

- **Example**:
  ```go
  var zeroTime time.Time
  fmt.Println("零时间:", zeroTime) // prints: 0001-01-01 00:00:00 +0000 UTC
  ```

#### 6. The limits of time strings

A time string must match the layout exactly. If the string contains extra spaces or characters, or the format does not line up, `time.Parse` returns an error.

- **Bad example**:
  ```go
  layout := "2006-01-02 15:04:05"
  value := "2024-07-27 15:30:00 extra" // extra characters present
  _, err := time.Parse(layout, value)
  if err != nil {
      fmt.Println("解析错误:", err) // parse error
  }
  ```

### Summary

One core rule: instead of a format string like `%Y-%m-%d`, you write the shape of each part of the reference time `2006-01-02 15:04:05`. The layout and the time string must line up exactly — one extra space or character and `time.Parse` returns an error. The zero value of `time.Time` is `0001-01-01 00:00:00 +0000 UTC`.

## References

- [time standard library](https://pkg.go.dev/time)

## Sibling pages

- [Advanced](/time/Advanced.md)
- [ConceptTime](/time/ConceptTime.md)
- [PkgTime](/time/PkgTime.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/time/Advanced.md)
- [ConceptTime](/time/ConceptTime.md)
- [PkgTime](/time/PkgTime.md)
- [Practice](/time/Practice.md)
- [TimeZone](/time/TimeZone.md)
- [TimerAndTicker](/time/TimerAndTicker.md)
