To publish your own Go package and make it public on GitHub, following versioning conventions, you generally need these steps:

### 1. Create a GitHub repository

1. Log in to GitHub, click the "+" in the top right corner, and select "New repository".
2. Fill in the repository name and description, select a public repository, and click "Create repository".

### 2. Initialize the local project

1. Create a new Go project directory locally:
   ```sh
   mkdir mypackage
   cd mypackage
   ```

2. Initialize the Go module:
   ```sh
   go mod init github.com/yourusername/mypackage
   ```

3. Create a Go source file, for example `mypackage.go`:
   ```go
   // mypackage.go
   package mypackage

   import "fmt"

   // Hello prints a greeting message
   func Hello() {
       fmt.Println("Hello, world!")
   }
   ```

4. Create a README file (optional but recommended):
   ````markdown
   # mypackage

   This is mypackage, a simple Go package for demonstration.

   ## Installation

   ```sh
   go get github.com/yourusername/mypackage
   ```

   ## Usage

   ```go
   package main

   import "github.com/yourusername/mypackage"

   func main() {
       mypackage.Hello()
   }
   ```
   ````

### 3. Commit the code to GitHub

1. Initialize the Git repository:
   ```sh
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. Connect the local repository to GitHub:
   ```sh
   git remote add origin https://github.com/yourusername/mypackage.git
   git push -u origin master
   ```

### 4. Version management

Version management for Go packages follows the semantic versioning (SemVer) specification. The version number format is `vMAJOR.MINOR.PATCH`, for example `v1.0.0`.

- **MAJOR** version: contains incompatible API changes.
- **MINOR** version: adds functionality and remains compatible with previous versions.
- **PATCH** version: makes backwards-compatible bug fixes.

### 5. Create a version tag

1. Create and push a tag locally, for example:
   ```sh
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. On the "Releases" page of the GitHub repository, click "Draft a new release", select the tag you just created, fill in the release notes, and click "Publish release".

### 6. Make sure the module path and version are compatible

1. Make sure the module path matches correctly:
   ```sh
   go mod tidy
   ```

2. Check that the module path in the `go.mod` file matches the GitHub repository. For example, `module github.com/yourusername/mypackage`.

### Example

Suppose the package you publish lives at `github.com/yourusername/mypackage` and you have created a `v1.0.0` tag. Users can install and use your package with the following command:
```sh
go get github.com/yourusername/mypackage@v1.0.0
```

### 7. Updating the package

When you update the package, modify the code and commit:
```sh
git commit -am "Add new feature"
```
Create a new version tag and push it:
```sh
git tag v1.1.0
git push origin v1.1.0
```
Then publish the new version to GitHub Releases.

The whole flow comes down to three steps: use `go mod init` to create the module, tag with semantic versioning as `vMAJOR.MINOR.PATCH`, and push to GitHub Releases. Users install a specific version with `go get package-path@version`.

## References

- [Official · Go Modules user guide](https://go.dev/doc/modules/)
- [Go Modules Reference](https://go.dev/ref/mod)
- [Official blog · Using Go Modules](https://go.dev/blog/using-go-modules)


## Sibling pages

- [Init](/mod/Init.md)
- [Mod](/mod/Mod.md)
- [Work](/mod/Work.md)
- [Package](/mod/Package.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Package](/mod/Package.md)
