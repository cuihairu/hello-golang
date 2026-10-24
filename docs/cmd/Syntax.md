### 2. Command-line Argument Basics

#### 2.1 Basic Principles of Argument Passing

Command-line arguments are parameters passed to a program through the command-line interface. At startup the program reads these arguments and parses them, which decides how it executes. In Go, you can access all the arguments passed to a program through the `os.Args` variable. `os.Args` is a string slice where the first element is the program's name and the elements after it are the arguments passed to the program.

#### 2.2 Types and Formats of Arguments

Command-line arguments mainly fall into two types: positional arguments and option arguments:

1. **Positional arguments**: Arguments passed to the program in order; their meaning depends on their position.
2. **Option arguments**: Used to pass configuration options or flags; they can be short or long options, with or without a value.

#### 2.3 POSIX Style

The POSIX standard defines the argument parsing conventions on Unix systems:

- Short options start with a single hyphen followed by a single character: `-o`
- Long options start with a double hyphen followed by a full word: `--option`
- Short options can be combined: `-abc` is equivalent to `-a -b -c`
- Option arguments can carry a value: `-o value` or `--option=value`

Example:

```shell
$ myprogram -a -b -c -o value --option=value
```

Parsing POSIX-style arguments in Go with the `flag` package:

```go
package main

import (
    "flag"
    "fmt"
)

func main() {
    aFlag := flag.Bool("a", false, "Option A")
    bFlag := flag.Bool("b", false, "Option B")
    cFlag := flag.Bool("c", false, "Option C")
    oFlag := flag.String("o", "", "Option O")
    optionFlag := flag.String("option", "", "Long Option")

    flag.Parse()

    fmt.Println("Option A:", *aFlag)
    fmt.Println("Option B:", *bFlag)
    fmt.Println("Option C:", *cFlag)
    fmt.Println("Option O:", *oFlag)
    fmt.Println("Long Option:", *optionFlag)
}
```

#### 2.4 Unix Style

Unix style generally follows the POSIX standard, but there are also some variants and tool-specific conventions. For example, the long-option-with-equals-sign format common in the GNU toolchain:

```shell
$ myprogram --option=value
```

Parsing Unix-style arguments with the `pflag` package:

```go
package main

import (
    "fmt"
    "github.com/spf13/pflag"
)

func main() {
    aFlag := pflag.Bool("a", false, "Option A")
    bFlag := pflag.Bool("b", false, "Option B")
    cFlag := pflag.Bool("c", false, "Option C")
    oFlag := pflag.String("o", "", "Option O")
    optionFlag := pflag.String("option", "", "Long Option")

    pflag.Parse()

    fmt.Println("Option A:", *aFlag)
    fmt.Println("Option B:", *bFlag)
    fmt.Println("Option C:", *cFlag)
    fmt.Println("Option O:", *oFlag)
    fmt.Println("Long Option:", *optionFlag)
}
```

#### 2.5 Windows Style

Command-line argument parsing on Windows systems differs somewhat from the POSIX standard: it typically uses a slash as the option prefix and supports several formats:

- Short options start with a slash: `/o`
- Option arguments can separate the value with a colon or an equals sign: `/o:value` or `/o=value`
- Long options also start with a slash: `/option`

Example:

```shell
C:\> myprogram /a /b /c /o:value /option=value
```

Handling Windows-style arguments with the `flag` package takes some custom parsing:

```go
package main

import (
    "flag"
    "fmt"
    "os"
    "strings"
)

func main() {
    var aFlag, bFlag, cFlag bool
    var oFlag, optionFlag string

    flag.BoolVar(&aFlag, "a", false, "Option A")
    flag.BoolVar(&bFlag, "b", false, "Option B")
    flag.BoolVar(&cFlag, "c", false, "Option C")
    flag.StringVar(&oFlag, "o", "", "Option O")
    flag.StringVar(&optionFlag, "option", "", "Long Option")

    for _, arg := range os.Args[1:] {
        if strings.HasPrefix(arg, "/") {
            kv := strings.SplitN(arg[1:], "=", 2)
            if len(kv) == 1 {
                kv = strings.SplitN(arg[1:], ":", 2)
            }
            switch kv[0] {
            case "a":
                aFlag = true
            case "b":
                bFlag = true
            case "c":
                cFlag = true
            case "o":
                if len(kv) > 1 {
                    oFlag = kv[1]
                }
            case "option":
                if len(kv) > 1 {
                    optionFlag = kv[1]
                }
            }
        }
    }

    fmt.Println("Option A:", aFlag)
    fmt.Println("Option B:", bFlag)
    fmt.Println("Option C:", cFlag)
    fmt.Println("Option O:", oFlag)
    fmt.Println("Long Option:", optionFlag)
}
```

#### 2.6 Basic Steps of Argument Parsing

When writing a command-line tool, parsing arguments typically involves these steps:

1. **Define arguments**: Decide which arguments the program accepts, and their types and meanings.
2. **Read arguments**: Use `os.Args` or a similar tool to read the arguments passed to the program.
3. **Parse arguments**: Parse according to the argument definitions, converting and validating types.
4. **Handle arguments**: Perform the corresponding operations based on the parsed arguments.

#### 2.7 Common Problems in Argument Parsing

Common problems include:

1. **Argument conflicts**: Different option arguments can conflict with each other, such as specifying both `--verbose` and `--quiet`.
2. **Missing required arguments**: Some arguments are required; if the user does not provide them, the program should report an error.
3. **Malformed argument values**: Users may pass values in the wrong format, such as giving a string where an integer is required.

Run one consolidated validation pass after parsing: missing arguments, malformed values, and option conflicts can all be caught at this step.

### Summary

The three styles differ in their option prefixes: POSIX uses single and double hyphens, Windows uses a slash; the value syntaxes are `-o value`, `--option=value`, and `/o:value` respectively. POSIX style is fine with `flag` alone; for Unix's long-option equals-sign format use `pflag`; Windows style requires parsing `os.Args` yourself on top of `flag`.

## References

- [flag standard library](https://pkg.go.dev/flag)
- [os/exec standard library](https://pkg.go.dev/os/exec)


## Sibling pages

- [Design](/cmd/Design.md)
- [Flag](/cmd/Flag.md)
- [Lib](/cmd/Lib.md)
- [Readme](/cmd/Readme.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Readme](/cmd/Readme.md)
