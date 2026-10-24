# Running and arguments
### Different command-line argument styles

Across operating systems and tools, the style of command-line arguments may differ. The main ones are:

#### POSIX style

The POSIX style is mainly used on Unix and Linux systems. Its characteristics are:

1. **Short options**:
    - Begin with a single dash (`-`) followed by a single letter.
    - Can be combined, e.g. `-abc` is equivalent to `-a -b -c`.
    - For example: `-h`, `-v`.

2. **Long options**:
    - Begin with a double dash (`--`) followed by a word or phrase.
    - For example: `--help`, `--version`.

3. **Arguments**:
    - An option can be followed by an argument value, separated by a space or an equals sign.
    - For example: `-o filename` or `-o=filename`.

Example:

```sh
ls -l -a
ls -la
grep --color=auto "pattern" file.txt
```

#### Windows style

The command-line argument style on Windows differs from POSIX in a few ways:

1. **Short and long options**:
    - Begin with a slash (`/`) followed by a single letter or a word.
    - For example: `/h`, `/help`.

2. **Arguments**:
    - An option can be followed by an argument value, separated by a colon (`:`) or a space.
    - For example: `/o:filename` or `/o filename`.

Example:

```sh
dir /s /p
find "pattern" file.txt /i
```

#### GNU style

The GNU style is an extension of POSIX and is common in GNU tools. Option syntax is the same as POSIX, while passing arguments allows more forms:

1. **Short and long options**:
    - Similar to POSIX.

2. **Arguments**:
    - Supports several ways of passing arguments, including with a space, with an equals sign, and with no separator.
    - For example: `--output=filename`, `--output filename`.

### How Go handles command-line arguments

In Go, handling command-line arguments usually uses the `flag` package. Here are a few common approaches:

#### Using the `flag` package

The `flag` package is a package in the Go standard library, used to parse command-line options and arguments.

```go
package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	// define the command-line arguments
	var help bool
	var name string

	flag.BoolVar(&help, "help", false, "show help information")
	flag.BoolVar(&help, "h", false, "show help information")
	flag.StringVar(&name, "name", "", "your name")

	// parse the command-line arguments
	flag.Parse()

	// handle the help request
	if help {
		fmt.Println("Usage: [options]")
		flag.PrintDefaults()
		os.Exit(0)
	}

	// print the passed argument values
	fmt.Printf("Hello, %s!\n", name)
}
```

In this example:

1. **Defining command-line arguments**:
    - Uses `flag.BoolVar` to define the boolean arguments `--help` and `-h`.
    - Uses `flag.StringVar` to define the string argument `--name`.

2. **Parsing command-line arguments**:
    - Uses `flag.Parse` to parse the command-line arguments.

3. **Handling the help request**:
    - If the `help` variable is `true`, print the help information and exit the program.

#### Running the example

Compile and run the program:

```sh
go build -o myapp
./myapp --name=John
```

Output:

```
Hello, John!
```

Use `--help` or `-h` to view the help information:

```sh
./myapp --help
```

Output:

```
Usage: [options]
  -h    show help information
  -help
        show help information
  -name string
        your name
```

## References

- [Go Official Documentation · Getting started (external link)](https://go.dev/doc/tutorial/getting-started)
- [Go Official Documentation · Create a module (external link)](https://go.dev/doc/tutorial/create-module)


## Sibling pages

- [BuildConstraint](/start/BuildConstraint.md)
- [Build](/start/Build.md)
- [Embed](/start/Embed.md)
- [Hello](/start/Hello.md)
- [Starter](/start/Starter.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Starter](/start/Starter.md)
