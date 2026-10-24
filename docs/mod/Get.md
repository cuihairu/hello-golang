In Go, installing packages and managing dependencies is done mostly through the `go get` command.

### Installing Go packages

There are three ways to install a package:

1. **Using the `go get` command (dependency management)**:
   ```sh
   go get <package-import-path>
   ```
   For example, to add the `github.com/gin-gonic/gin` dependency to the current module, you can use:
   ```sh
   go get github.com/gin-gonic/gin
   ```

   Note: starting with Go 1.17, `go get` no longer builds and installs packages; it only adjusts the dependencies in `go.mod`. If you need to install a command-line tool (an executable), use `go install` with a version suffix:
   ```sh
   go install golang.org/x/tools/cmd/goimports@latest
   ```

2. **Using the `go mod` command**:
   When managing dependencies with Go Modules, you can add a dependency in the `go.mod` file, then use `go mod tidy` or `go mod download` to download the dependency packages.
   ```sh
   go mod tidy
   ```
   or
   ```sh
   go mod download
   ```

3. **Downloading and installing a package manually**:
   You can clone a package from its source repository and place it under the appropriate `GOPATH` directory, then run `go install`.
   ```sh
   git clone <package-repo-url>
   cd <package-directory>
   go install
   ```

### How `go get` works

The main job of the `go get` command is to fetch a Go package from a remote repository and install it into the local `GOPATH` or the directory managed by `go.mod`. The process goes like this:

1. **Parsing the package path**:
   `go get` parses the package path you provide and determines the remote repository that holds it. For example, the path `golang.org/x/tools/cmd/goimports` resolves to the official Golang tools repository.

2. **Fetching repository information**:
   `go get` extracts version control information (such as Git or Mercurial) from the parsed package path and fetches the latest code from that repository.

3. **Downloading the package code**:
   `go get` uses the corresponding version control tool (such as Git) to download the package code into the local module cache directory (by default under `$GOPATH/pkg/mod`).

4. **Updating dependencies**:
   In Go 1.17 and later, `go get` only downloads the source code and updates the dependencies — it does **not** build or install the package. When you need to install an executable, use `go install <package>@<version>`.

5. **Updating the dependency files**:
   In Go Modules mode, `go get` updates the `go.mod` and `go.sum` files to make sure all dependency versions are consistent.

### Example

Suppose you want to install the `github.com/gin-gonic/gin` package. You can run:
```sh
go get github.com/gin-gonic/gin
```

The `go.mod` file will contain something like this:
```go
module your_module_name

go 1.16

require (
    github.com/gin-gonic/gin v1.7.4
)
```

The `go.sum` file records the package's hash and its dependency relationships:
```plaintext
github.com/gin-gonic/gin v1.7.4 h1:ZjAtzNWBc+t1OXcMGYWZzwE7Em8oUVQz1SoNQoVDhnQ=
github.com/gin-gonic/gin v1.7.4/go.mod h1:ZZFzY1G5e/oDpUsGtcj0FJ/h4ug9Qt68N/m9uITtdlI=
```

Versions live in `go.mod`, checksums live in `go.sum`. When a dependency goes wrong, that's the two files to check.

## References

- [Official · Go Modules user guide](https://go.dev/doc/modules/)
- [Go Modules Reference](https://go.dev/ref/mod)
- [Official blog · Using Go Modules](https://go.dev/blog/using-go-modules)


## Sibling pages

- [Init](/mod/Init.md)
- [Mod](/mod/Mod.md)
- [Work](/mod/Work.md)
- [Import](/mod/Import.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Import](/mod/Import.md)
