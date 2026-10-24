# Date and time

Time shows up in programs in a few places: recording when an event happened, scheduling tasks, computing intervals, and stamping logs. Get the format or timezone wrong and none of it works.

#### 1.1 Why time handling matters

The complexity of time handling comes in these shapes:

- **Recording and displaying time**: many apps need to record when a user acted, generate timestamps, or display the current time. That means the program has to fetch and format time accurately.
    
- **Scheduling and delays**: scheduled tasks and delayed operations are common in many apps. Timers can trigger periodic events, and delaying a function's execution controls when a task runs.
    
- **Cross-timezone handling**: in global apps, handling time and timezone conversion across regions is mandatory. Correct timezone and daylight saving handling avoids a lot of potential problems.
    
- **Computing intervals**: measuring time differences and the duration of operations is a frequent need in performance analysis and optimization.
    

#### 1.2 Overview of time handling in Go

Go's standard library `time` package handles dates and times, and it has these properties:

- **Covers common operations**: fetching, formatting, parsing, and manipulating time all live in one package.
    
- **Fixed layout**: formatting and parsing both work from a single fixed reference layout, `2006-01-02 15:04:05`.
    
- **Timezone support**: loading timezones, converting between them, and daylight saving are all handled.
    
- **Intervals**: the `Duration` type represents a span of time.
    
- **Timers and tickers**: the `Timer` and `Ticker` types handle one-off delays and periodic events.

## Concepts related to time

Organized by concept: date and time representation, timestamps, timezones, local time and UTC, daylight saving, formats, intervals, addition and comparison, calendar systems.

### 1. **Date and time representation**

- **Date**: usually expressed as a combination of year, month, and day. For example, 27 July 2024 is written as `2024-07-27`.
- **Time**: usually expressed as a combination of hours, minutes, and seconds. For example, 3:15:30 PM is written as `15:15:30`.
- **Date-time**: date and time combined. For example, `2024-07-27T15:15:30` (ISO 8601) means 3:15:30 PM on 27 July 2024.

### 2. **Timestamps**

- **Timestamp**: the number of seconds or milliseconds since a fixed reference point (such as 00:00:00 UTC on 1 January 1970, the "Unix epoch"). Used to compute intervals or pass time data between systems.

### 3. **Timezones**

- **Timezone**: the time setting for a region on Earth. For example, UTC+8 means eight hours ahead of Coordinated Universal Time (UTC). Timezone handling affects both the display and the arithmetic of time.

### 4. **Local time and Coordinated Universal Time (UTC)**

- **Local time**: time that depends on the timezone setting. For example, when you are in New York, local time is Eastern Time (EST/EDT) and can differ from UTC by a different offset.
- **Coordinated Universal Time (UTC)**: a standard time unaffected by timezones, used to unify time across different geographic locations.

### 5. **Daylight Saving Time (DST)**

- **Daylight Saving Time (DST)**: some regions move the clock forward by one hour in summer to make better use of daylight. The start and end times can differ and need special handling.

### 6. **Date and time formats**

- **Standard formats**: such as ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`), the standard way to represent date and time.
- **Custom formats**: for example, `MM/DD/YYYY` or `DD-MM-YYYY`; you can tailor the display format of date and time to your needs.

### 7. **Intervals and durations**

- **Interval**: the difference between two points in time. For example, 2 hours 30 minutes.
- **Duration**: how long an event lasts. For example, some task may take 5 minutes.

### 8. **Date and time arithmetic**

- **Addition and subtraction**: add to or subtract from a date or time. For example, computing the date 30 days from now, or the time 2 hours from now.
- **Comparison**: compare the order of two dates or times.

### 9. **Calendar systems**

- **Solar calendar (Gregorian)**: the widely used calendar system, based on the period of the Earth's orbit around the Sun.
- **Lunar calendar**: such as the Chinese lunar calendar, based on the cycles of the Moon.


### Summary
Every one of these concepts has a home in the `time` package: intervals use `Duration`, formatting uses the fixed `2006-01-02 15:04:05` layout, and timezones plus daylight saving come with built-in support.

## References

- [time standard library](https://pkg.go.dev/time)

## Sibling pages

- [Advanced](/time/Advanced.md)
- [FormatAndParse](/time/FormatAndParse.md)
- [PkgTime](/time/PkgTime.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/time/Advanced.md)
- [FormatAndParse](/time/FormatAndParse.md)
- [PkgTime](/time/PkgTime.md)
- [Practice](/time/Practice.md)
- [TimeZone](/time/TimeZone.md)
- [TimerAndTicker](/time/TimerAndTicker.md)
