# Goland
Goland is an integrated development environment (IDE) developed by JetBrains specifically for Go.

### 1. Install Goland

1. **Download Goland:**
   - Visit JetBrains' official website at the [Goland download page](https://www.jetbrains.com/go/download/) and download the installer for your operating system.

2. **Install Goland:**
   - Depending on your operating system, run the downloaded installer and follow the installation wizard to finish.

3. **Activate Goland:**
   - After launching Goland you need to activate the product. You can use a trial version (usually 30 days) or activate with a purchased license.

### 2. Configure the Go environment

1. **Install Go:**
   - Visit the [Go official site](https://go.dev/dl/) and download and install the Go SDK for your operating system.

2. **Configure Go environment variables:**
   - Configure the `GOPATH` and `GOROOT` environment variables according to the Go installation guide.

3. **Configure Goland:**
   - Launch Goland, click `File > Settings` (Windows/Linux) or `GoLand > Preferences` (MacOS), then navigate to `Go > GOROOT` and `Go > GOPATH`, and make sure they point to the correct Go SDK directory and workspace directory.

### 3. Create and run a Go project

1. **Create a new project:**
   - Launch Goland and click `File > New Project`.
   - Choose the `Go` project type, set the project name and location, select the Go SDK, and click `Create`.

2. **Write Go code:**
   - In the project structure, right-click the `src` directory, choose `New > Go File`, and create a new `.go` file.
   - Write your Go code, for example a simple `main.go` file:
     ```go
     package main

     import "fmt"

     func main() {
         fmt.Println("Hello, GoLand!")
     }
     ```

3. **Run the Go code:**
   - Right-click the file in the code editor and choose `Run 'main.go'`.
   - Or click the green triangle button at the top of the editor to run the program.

### 4. Use Goland's advanced features

1. **Code navigation:**
   - Use `Ctrl + Click` to jump to the definition of a function or variable.
   - Use `Ctrl + N` to search for and open a Go file.
   - Use `Ctrl + Shift + N` to search for and open any file.

2. **Code refactoring:**
   - Right-click a variable, function, or type in the code and choose `Refactor` to rename, move, or otherwise refactor it.

3. **Debugging code:**
   - Click to the left of a line number to set a breakpoint.
   - While running, click `Run > Debug` or use the debug button to start debug mode.
   - In debug mode you can step through code, view variable values, and the call stack.

4. **Plugins and tools:**
   - Install plugins through `File > Settings > Plugins`, such as the `Go Modules` plugin.
   - Use the built-in `Terminal`, `Database Tools`, and `Version Control` (such as Git) for development and management.

### 5. Tips to improve efficiency

1. **Use keyboard shortcuts:**
   - `Ctrl + D` duplicates a line; `Ctrl + /` comments or uncomments a line of code.

2. **Code templates:**
   - Use code templates to auto-generate commonly used snippets, configured in `File > Settings > Editor > Live Templates`.

3. **Code inspection and hints:**
   - Goland provides real-time code inspection and smart hints, helping you find and fix code problems quickly.

## References

- [Official · Installing and managing the Go toolchain](https://go.dev/doc/manage-install)
- [Go Official Documentation · Getting started (external link)](https://go.dev/doc/tutorial/getting-started)
- [Official · Go Modules guide](https://go.dev/doc/modules/)

## Sibling pages

- [Env](/env/Env.md)
- [Install](/env/Install.md)
- [GOPROXY](/env/GOPROXY.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [GOPROXY](/env/GOPROXY.md)
