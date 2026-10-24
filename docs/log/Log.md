### Overview

Logs record a program's running state, error messages and performance data. When something breaks, logs are usually the first-line evidence; without them, investigation is just guessing.

#### What Logs Are Used For

1. **Debugging and troubleshooting**: record the detailed runtime process, then replay the timeline after an error.
2. **Performance monitoring**: record metrics such as latency, and find out where things are slow.
3. **Security auditing**: leave a trail of user actions and system events.
4. **Operations support**: in production, judge whether a service is healthy and which machine a failure started on.
5. **Business analysis**: measure actual user behavior and how business flows really run.

#### An Overview of Logging Solutions in Go

Go's logging solutions come in three layers: the standard library, third-party libraries, and centralized tools.

1. **The Go standard library `log`**:
   - Provides basic log output, supporting a prefix, flags, and output redirection.
   - Has no log levels and no structured logging; adequate, but only for simple cases.

2. **Third-party logging libraries**:
   - **`logrus`**: supports structured logging, log levels and a hook mechanism; fits cases with complex log formats.
   - **`zap`**: performance-optimized, supports structured logging and log levels; fits high-throughput services.
   - **`zerolog`**: logs as JSON with a small allocation footprint; fits latency-sensitive cases.

3. **Log aggregation and centralized management tools**:
   - **`fluentd`** and **`logstash`**: gather logs scattered across machines into one place for unified searching.
   - **Cloud log services**: such as AWS CloudWatch and Google Stackdriver, which collect, store and analyze, suited to large-scale distributed systems.

## References

- [log standard library](https://pkg.go.dev/log)
- [Official blog · Structured Logging with slog](https://go.dev/blog/slog)

## Sibling pages

- [Aggregation](/log/Aggregation.md)
- [LibLog](/log/LibLog.md)
- [ModLog](/log/ModLog.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Aggregation](/log/Aggregation.md)
- [LibLog](/log/LibLog.md)
- [ModLog](/log/ModLog.md)
