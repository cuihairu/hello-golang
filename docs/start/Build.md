# Compiling
In Go, compiling is the process of converting Go source code into an executable file. Overall it breaks down into a few stages: compile, assemble, and link.

### 1. Steps of Go program compilation

#### 1.1 Lexical Analysis

The Go compiler first performs lexical analysis on the source code, splitting it into tokens. These tokens are the smallest units of a programming language, such as keywords, variable names, and operators.

**Purpose**: generate a token stream to prepare for the subsequent syntax analysis.

#### 1.2 Syntax Analysis

In the syntax analysis stage, the compiler converts the token stream into an abstract syntax tree (AST), which represents the syntactic structure of the program.

**Purpose**: verify the correctness of the syntax and produce a structure that is easier to process further.

#### 1.3 Semantic Analysis

In the semantic analysis stage, the compiler checks the semantic rules in the AST, such as type checking, variable declarations, and scope checking.

**Purpose**: ensure the logical correctness of the program and collect type information.

#### 1.4 Intermediate Code Generation

The compiler converts the AST into intermediate code, a lower-level representation that makes optimization and target code generation easier.

**Purpose**: produce an intermediate form closer to machine language, preparing for optimization.

#### 1.5 Optimization

In the optimization stage, the compiler optimizes the intermediate code, for example by removing dead code, constant folding, and loop optimization.

**Purpose**: improve the efficiency and performance of the generated code.

#### 1.6 Target Code Generation

The compiler converts the optimized intermediate code into assembly code.

**Purpose**: generate assembly code for a specific platform.

#### 1.7 Assembly

The assembler converts the assembly code into target machine code.

**Purpose**: generate binary machine code.

#### 1.8 Linking

The linker merges the different target files and library files into a single executable file.

**Purpose**: produce the final executable file and resolve external symbol references.

### 2. Compilation parameters of Go

In Go, the `go build` command is used to compile programs. The following are some commonly used compilation parameters and their purposes:

#### 2.1 `-o` 

Specifies the name of the output file.

```sh
go build -o myapp main.go
```

#### 2.2 `-v`

Shows detailed information about the compilation process.

```sh
go build -v
```

#### 2.3 `-x`

Shows the commands executed during the compilation process.

```sh
go build -x
```

#### 2.4 `-race`

Enables data race detection (race condition detection).

```sh
go build -race
```

#### 2.5 `-gcflags`

Extra compilation options passed to the Go compiler, usually for debugging and optimization. For example, to disable inlining:

```sh
go build -gcflags="-l"
```

#### 2.6 `-ldflags`

Options passed to the linker. For example, to set version information on the executable:

```sh
go build -ldflags="-X 'main.version=1.0'"
```

#### 2.7 `-tags`

Sets build tags, used for selective compilation.

```sh
go build -tags="debug"
```

#### 2.8 `-mod`

Sets how dependency modules are handled; it can be `readonly`, `vendor`, and so on.

```sh
go build -mod=readonly
```

### Example

Here is an example that combines several parameters:

```sh
go build -o myapp -v -x -race -gcflags="-N -l" -ldflags="-X 'main.version=1.0'" -tags="debug"
```

This command compiles the `main.go` file, produces an executable named `myapp`, and enables verbose output, shows the executed commands, enables data race detection, disables optimization and inlining, sets version information, and compiles with the `debug` tag.

## References

- [Go Official Documentation · Getting started (external link)](https://go.dev/doc/tutorial/getting-started)
- [Go Official Documentation · Create a module (external link)](https://go.dev/doc/tutorial/create-module)

## Sibling pages

- [BuildConstraint](/start/BuildConstraint.md)
- [Embed](/start/Embed.md)
- [Hello](/start/Hello.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Embed](/start/Embed.md)
- [Hello](/start/Hello.md)
- [Run](/start/Run.md)
- [Starter](/start/Starter.md)
- [Structure](/start/Structure.md)
