
## Installing Go

### 1. Download and install Go from the official site

#### Windows
1. Open the [Go download page](https://go.dev/dl/).
2. Select and download the installer for Windows (for example: `go1.22.5.windows-amd64.msi`).
3. Double-click the downloaded MSI file and follow the installation wizard to complete the install.

#### Linux
1. Open the [Go download page](https://go.dev/dl/).
2. Select and download the installer for Linux (for example: `go1.22.5.linux-amd64.tar.gz`).
3. Open a terminal and run the following command to extract and install Go:
   ```sh
   tar -C /usr/local -xzf go1.22.5.linux-amd64.tar.gz
   ```

#### macOS
1. Open the [Go download page](https://go.dev/dl/).
2. Select and download the installer for macOS (for example: `go1.22.5.darwin-amd64.pkg`).
3. Double-click the downloaded PKG file and follow the installation wizard to complete the install.

### 2. Set up environment variables

#### Windows
1. Open "Control Panel" -> "System and Security" -> "System" -> "Advanced system settings".
2. In the "System Properties" window, click "Environment Variables".
3. In the "System variables" section, find and select the "Path" variable and click "Edit".
4. Click "New", add Go's installation path (the MSI default installs to `C:\Program Files\Go`, so you need to add `C:\Program Files\Go\bin`), then click "OK" to save.

#### Linux
1. Open a terminal and edit your shell configuration file (for example: `~/.bashrc` or `~/.profile` or `~/.zshrc`), adding the following line:
   ```sh
   export PATH=$PATH:/usr/local/go/bin
   ```
2. Save the file and run the following command to apply the change:
   ```sh
   source ~/.bashrc  # or source ~/.profile or source ~/.zshrc
   ```

#### macOS
1. Open a terminal and edit your shell configuration file (for example: `~/.bash_profile` or `~/.zshrc`), adding the following line:
   ```sh
   export PATH=$PATH:/usr/local/go/bin
   ```
2. Save the file and run the following command to apply the change:
   ```sh
   source ~/.bash_profile  # or source ~/.zshrc
   ```

### 3. Verify the installation
Open a terminal or command prompt and run the following command to verify that Go was installed successfully:
```sh
go version
```

### Installing Go with a package manager

#### macOS with Homebrew
1. Open a terminal and run the following command to install Go:
   ```sh
   brew install go
   ```
2. After installation, Homebrew automatically adds Go's path to your PATH variable, so you can verify directly:
   ```sh
   go version
   ```

#### Windows with Scoop
1. Open PowerShell and run the following command to install Scoop:
   ```sh
   iwr -useb get.scoop.sh | iex
   ```
2. Use Scoop to install Go:
   ```sh
   scoop install go
   ```
3. Verify the installation:
   ```sh
   go version
   ```

Run `go version` once after installing — if it prints a version number, the install and `PATH` are both set up.

## References

- [Official · Installing and managing the Go toolchain](https://go.dev/doc/manage-install)
- [Go Official Documentation · Getting started (external link)](https://go.dev/doc/tutorial/getting-started)
- [Official · Go Modules usage guide](https://go.dev/doc/modules/)

<!-- BACKLINKS-AUTO -->
## Related pages

- [GOPROXY](/env/GOPROXY.md)
- [Goland](/env/Goland.md)
- [Modules](/env/Modules.md)
- [Tools](/env/Tools.md)
- [Vim](/env/Vim.md)
- [ide](/env/ide.md)
- [vscode](/env/vscode.md)
- [glossary](/glossary.md)
