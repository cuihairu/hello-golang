# VsCode
Setting up a Go development environment in VS Code: install VS Code and Go, add Go's bin directory to your environment variables, then install the Go extension and tools:

### 1. Install VS Code
- Visit the [VS Code official site](https://code.visualstudio.com/) and download and install the version for your operating system.

### 2. Install Go language development tools
- Visit the [Go official site](https://go.dev/dl/) and download and install the Go version for your operating system.

### 3. Configure environment variables
- After installation, add Go's install path to the system environment variables so the `go` command is available in the terminal.
  - **Windows**:
    1. Open "Control Panel" -> "System and Security" -> "System" -> "Advanced system settings".
    2. In the "System Properties" window, click "Environment Variables".
    3. Find `Path` under "System variables", click "Edit", then add Go's install path (the MSI installer puts it in `C:\Program Files\Go` by default, so what you add is `C:\Program Files\Go\bin`).
  - **macOS** and **Linux**:
    - Edit `~/.bashrc` or `~/.zshrc` and add the following:
      ```sh
      export PATH=$PATH:/usr/local/go/bin
      ```
    - After saving the file, run `source ~/.bashrc` or `source ~/.zshrc` to apply the changes.

### 4. Install the Go extension
- Open VS Code and click the extensions icon in the activity bar on the left (or press `Ctrl+Shift+X`).
- Search for `Go` in the extensions marketplace, find the extension developed by the Go team, and click "Install".

### 5. Set GOPATH
- After opening VS Code, press `Ctrl+,` to open settings and search for `GOPATH`.
- Set `GOPATH` to your working directory, such as `C:\Users\YourName\go` (Windows) or `~/go` (macOS/Linux).

### 6. Install Go tools
- Open the command palette in VS Code (press `Ctrl+Shift+P`), type `Go: Install/Update Tools` and press Enter.
- Select all tools and click "OK" to install.

### 7. Create and run a simple Go program
- Create a new project directory under `GOPATH`, for example: `C:\Users\YourName\go\src\hello`.
- Open that directory in VS Code, create a `main.go` file, and enter the following code:
  ```go
  package main

  import "fmt"

  func main() {
      fmt.Println("Hello, World!")
  }
  ```
- Open the terminal (press `Ctrl+``) and run the following command to execute the program:
  ```sh
  go run main.go
  ```

### 8. Debug a Go program
- Set breakpoints: click beside a line number in the code to set a breakpoint.
- Start debugging: click the debug icon in the activity bar on the left, click "Create a launch.json file", and select `Go`.
- Once configured, click "Start Debugging" (the green arrow icon) to begin debugging the program.

### 9. Format code
- In VS Code, Go code is formatted automatically on save by default. You can format manually as follows:
  - Right-click the code file and select "Format Document".
  - Or press the shortcut `Shift+Alt+F`.

### 10. Code completion and linting
- The Go extension in VS Code includes code completion and linting out of the box, automatically suggesting completions and flagging errors as you type.

### Common problems and fixes
- If a tool installation fails, search for and run `Go: Install/Update Tools` in the command palette, and select the tools you need to reinstall.
- If code hints and completion misbehave, try reloading VS Code (press `Ctrl+Shift+P`, type `Reload Window` and press Enter).

Once the tools are installed, see the [VS Code Go extension docs](https://github.com/golang/vscode-go) for more on using the extension.

## References

- [Official · Installing and managing the Go toolchain](https://go.dev/doc/manage-install)
- [Go Official Documentation · Getting started (external link)](https://go.dev/doc/tutorial/getting-started)
- [Official · Go Modules guide](https://go.dev/doc/modules/)


## Sibling pages

- [Env](/env/Env.md)
- [Install](/env/Install.md)
- [GOPROXY](/env/GOPROXY.md)
- [ide](/env/ide.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ide](/env/ide.md)
