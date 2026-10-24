# Native fuzzing: FuzzXxx and go test -fuzz

Go has built-in fuzzing in the standard toolchain since **1.18**, using coverage guidance to walk the input branches a human would not think of. I had previously only documented the external go-fuzz toolchain in `docs/zh/test/Lib.md`; the notes on native fuzzing are added here from the official `/doc/fuzz/` page and the Fuzzing page (external link), with material fetched on 2026-10-08.

## 1. The problem it solves

Fuzzing is automated testing that keeps mutating a program's inputs to find bugs. The official rationale is that it reaches edge cases humans tend to miss, which makes it especially valuable for finding security vulnerabilities. Native fuzz tests are supported by OSS-Fuzz.

## 2. Writing rules (from the official Requirements section)

- A test function must be named `FuzzXxx`, take only a single `*testing.F`, and have no return value.
- A fuzz test must live in a `_test.go` file.
- The fuzz target is registered via `(*testing.F).Fuzz`; its first parameter is `*testing.T`, followed by the fuzz parameters, with no return value, and each fuzz test can have only one target.
- The types of the seed corpus must exactly match the fuzz parameters and appear in the same order; calls to `(*testing.F).Add` and corpus files under `testdata/fuzz` both count.
- The only allowed parameter types are: `string`, `[]byte`, integer types of all sizes, `rune`, unsigned integer types of all sizes, `float32`, `float64`, and `bool`.

The official advice: a fuzz target should be fast and deterministic, so the engine can keep up and new failures can be reproduced. Targets are called in parallel by multiple workers and in arbitrary order, so do not let state leak across calls and do not depend on global state.

## 3. Two ways to run it

| Run mode | Command | Behavior |
| --- | --- | --- |
| As a unit test | `go test` | Each seed corpus entry is fed to the target once; any failure reports an error and exits |
| Real fuzzing | `go test -fuzz=FuzzTestName` | `-fuzz` takes a regex; the matching fuzz test starts mutating input continuously |

One example, fuzzing URL parsing:

```go
// fuzz_test.go
package example

import (
    "net/url"
    "testing"
)

func FuzzParse(f *testing.F) {
    f.Add("https://example.com/path?q=1")
    f.Fuzz(func(t *testing.T, raw string) {
        u, err := url.Parse(raw)
        if err != nil {
            t.Skip()
        }
        _ = u.String()
    })
}
```

Add seed corpus entries with `f.Add`, or place them under `testdata/fuzz/FuzzParse/`. A failing input found during fuzzing is written back to the corpus directory, so the next `go test` reproduces it directly.

## 4. How this relates to other pages in this repo

| Topic | Page |
| --- | --- |
| Unit tests and subtests | `docs/zh/test/Test.md`, `docs/zh/test/Advanced.md` |
| Table-driven tests | `docs/zh/test/Practice.md` |
| Benchmarks | `docs/zh/test/Benchmark.md` |
| Coverage | `docs/zh/test/Cover.md` |
| The external go-fuzz toolchain | `docs/zh/test/Lib.md` |
| The security-side view of fuzzing | `docs/zh/security/Security.md` |

## 5. When it is worth writing

It pays off most for parsers that take input from the outside (URL, JSON, templates, regex, protocol decoding) — one line of `f.Add` plus a target is enough. For internal functions whose inputs are a fixed enumeration, running fuzz is more likely to just burn CPU; a table-driven test is more direct.

## Sources

1. https://golang.google.cn/doc/fuzz/ — Go Fuzzing: built in since 1.18, coverage-guided, Requirements and advice, the two ways to run, OSS-Fuzz (fetched 2026-10-08)
2. https://golang.google.cn/doc/tutorial/fuzz.html — the Fuzzing page (external link)
3. https://golang.google.cn/security/ — the security page lists fuzzing as a way to find vulnerabilities

## References

- [testing standard library](https://pkg.go.dev/testing)
- [Go Official Documentation · Add a test (external link)](https://go.dev/doc/tutorial/add-a-test)
- [Official · Fuzzing (security)](https://go.dev/doc/security/fuzz/)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
- [knowledge](/knowledge.md)
- [Advanced](/test/Advanced.md)
- [BaseTest](/test/BaseTest.md)
- [Benchmark](/test/Benchmark.md)
- [Cover](/test/Cover.md)
- [Example](/test/Example.md)
- [Lib](/test/Lib.md)
- [Practice](/test/Practice.md)
